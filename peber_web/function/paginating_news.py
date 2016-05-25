# coding=utf-8
from goose import Goose
from newspaper import Article
# Special case for detik tekno news
from bs4 import BeautifulSoup
# Untuk ubah format tanggal jadi tidak naive atau tambah localization
from django.utils import timezone
import pytz
# Menangani karakter no ASCII
from unidecode import unidecode


# noinspection PyShadowingNames
def extract_detik(article_soup):
	print ("{detik} paginating news extractor (detik.com)")

	# List untuk menampung teks detik.
	detik_data = []

	tag_to_del = ['strong', 'b', 'None']
	for tag in article_soup.find_all(recursive=False):  # Ambil hanya satu level
		if tag.name == 'div':
			tag.extract()

		if tag.name == 'em':
			if "Baca" in tag.strong.string:
				tag.extract()

		if tag.name == 'span':
			tag.extract()

		if tag.name in tag_to_del:
			# tag.replace_with(tag.encode_contents())
			if tag.name == 'b':
				if tag.strong.name == 'strong':
					tag.strong.string += ", \n"
					tag.unwrap()
					continue
				tag.unwrap()
			tag.unwrap()
			print "Tag %s found" % tag.name

	# print u"\n\n%s\n" % article_soup.prettify()

	for string in article_soup.stripped_strings:
		detik_data.append(string)

	# article_soup.find(attrs={"class": "leftside"}).extract()
	# print "HASIL:\n" , article_soup.prettify()

	# if len(detik_data) != 0:
	# 	for i, teks in enumerate(detik_data):
	# 		if i == 0:
	# 			if teks.find('-') != -1:
	# 				detik_data.pop(i)
	# 		if i == 1:
	# 			if teks.find('-') != -1:
	# 				detik_data.pop(i)
	# 				detik_data.pop(0)
	# 			break

	return detik_data


# noinspection PyShadowingNames
def extract_pagination_liputan6(liputan6_soup_data):
	print ("{Liputan6.com} paginating news")
	liputan6_data = []
	liputan6_urls = []

	goose_instance = Goose()

	# Ambil url-url berita
	pagination_list_soup = liputan6_soup_data.find("ul", class_="read-page--multi-page--pagination__list")
	for a_tag in pagination_list_soup.find_all('a'):
		url_href = a_tag.get('href')
		liputan6_urls.append(url_href)

		# Memperoleh data dari internet
		article = goose_instance.extract(url=url_href)
		raw_html = article.raw_html
		liputan6_soup_data = BeautifulSoup(raw_html)

		# Ambil kontent
		liputan6_content_soup = liputan6_soup_data.find("div", class_="read-page__content-body text-detail")
		if liputan6_content_soup is not None:

			for tag in liputan6_content_soup.find_all(reversed=False):
				# Deteksi setiap tag p
				if tag.name == 'p':
					# Hapus pub signature pada tag b dalam tag p (Liputan6.com)
					b_soup = tag.find('b')
					if b_soup is not None:
						if b_soup.text.lower().find('liputan6') != -1:
							print("{liputan6} Signature ditemukan dlm B: %s" % b_soup.text)
							b_soup.extract()

					# Masukkan teks dalam list
					tag_text = tag.get_text(' ').strip()
					if len(tag_text) > 10:
						liputan6_data.append(unidecode(tag_text))

	# bersihkan tanda dash pada index pertama.
	# liputan6_cuts = liputan6_data[0].split('-', 1)
	# if len(liputan6_cuts) == 2:
	# 	liputan6_data[0] = liputan6_cuts[1].strip()

	return liputan6_data


# noinspection PyShadowingNames
def extract_pagination_kompas(kompas_soup_data):
	print ("{kompas.com} paginating news")
	kompas_data = []

	# Ambil URL "?page=all", untuk versi lengkap
	# berita
	single_page_url = None
	for tag in kompas_soup_data.find_all('a'):
		url_href = tag.get('href')
		if url_href.find("page=all") != -1:
			single_page_url = url_href
			break

	# Ambil data dari internet menggunakan URL Single Page
	if single_page_url is not None:
		goose_instance = Goose()
		article = goose_instance.extract(url=single_page_url)
		raw_html = article.raw_html
		kompas_soup_data = BeautifulSoup(raw_html)

		# Parse teks dari tag yg diperoleh
		kompas_text_soup = kompas_soup_data.find('div', class_="kcm-read-text")
		if kompas_text_soup is not None:
			for tag in kompas_text_soup.find_all(recursive=False):
				if tag.name == 'div':
					tag.extract()

				# Jika tag strong tidak dalam p tapi di div konten
				if tag.name == "strong":
					if tag.text.lower().find('kompas') != -1:
						print("{kompas} Signature ditemukan dlm div: %s" % tag.text)
						tag.extract()

				if tag.name == 'p':
					# Hapus pub signature pada tag b dalam tag p (kompas.com)
					for strong_tag in tag.find_all('strong'):
						strong_soup = strong_tag
						if strong_soup is not None:
							if strong_soup.text.lower().find('kompas') != -1:
								print("{kompas} Signature ditemukan dlm B: %s" % strong_soup.text)
								strong_soup.extract()

							if strong_soup.a is not None:
								tag.extract()

							if strong_soup.text.find('Baca juga:') != -1:
								print("Teks baca juga ditemukan")
								strong_soup.extract()

					# Memastikan string kosong di skip
					# sehingga boleh masuk dalam list
					tag_text = tag.get_text().strip()
					if len(tag_text) > 5:
						kompas_data.append(unidecode(tag_text))

	# print(kompas_data[:3])

	# Periksa apakah list teks berita ada, jika ada
	# Hilangkan tanda pada first list 
	if len(kompas_data) != 0:

		split_1_dash = kompas_data[0].split('-', 1)
		split_2_dash = kompas_data[0].split('--', 1)

		# Cek split 1 dash
		if len(split_1_dash) == 2:
			kompas_data[0] = split_1_dash[1].strip()
		# Cek split 2 dash
		if len(split_2_dash) == 2:
			kompas_data[0] = split_2_dash[1].strip()

	return kompas_data


# noinspection PyShadowingNames
def extract_single_kompas(kompas_content_soup):
	print ("{kompas.com} single paged news")
	kompas_data = []
	if kompas_content_soup is not None:

		for tag in kompas_content_soup.find_all(recursive=False):
			# Jika tag strong tidak dalam p tapi di div konten
			if tag.name == "strong":
				if tag.text.lower().find('kompas') != -1:
					print("{kompas} Signature ditemukan dlm div: %s" % tag.text)
					tag.extract()
					# Alt teks jika tidak ada tag p dalam konten divs (Feb 2nd)
					alt_text = unidecode(kompas_content_soup.get_text().strip())

			if tag.name == 'p':
				# Hapus pub signature pada tag b dalam tag p (kompas.com)
				# dan tag-tag strong yang biasanya tidak mengandung teks berita
				for strong_tag in tag.find_all('strong'):
					strong_soup = strong_tag
					if strong_soup is not None:
						if strong_soup.text.lower().find('kompas') != -1: 
							print("{kompas} Signature ditemukan dlm B: %s" % strong_soup.text)
							strong_soup.extract()

						if strong_soup.a is not None:
							strong_soup.extract()

						if strong_soup.text.find('Baca juga:') != -1:
							print("Teks baca juga ditemukan")
							strong_soup.extract()

				# Memastikan string kosong dan teks skunder di skip
				# sehingga boleh masuk dalam list
				# cth: len("Baca juga") == 9 diskip.
				tag_text = tag.get_text().strip()
				if len(tag_text) > 10:
					kompas_data.append(unidecode(tag_text))

		# Periksa apakah list teks berita ada, jika tidak
		# lakukan alternatif teknik ekstraksi
		if len(kompas_data) == 0:
			print("Alternative way!")
			print(alt_text)
			print(len(alt_text))

			# Menyamakan -- (double dash) menjadi - (dash) (Feb 2nd)
			alt_text.replace('--', '-')

			# alt_text = unidecode(kompas_content_soup.get_text('\n').strip())
			# alt_text = unidecode("\n".join(kompas_content_soup.strings).strip())

			# if len(alt_text.split('--', 1)) == 2:
			# 	alt_text = alt_text.split('--', 1)[1].strip()

			# if len(alt_text.split('-', 1)) == 2:
			# 	alt_text = alt_text.split('-', 1)[1].strip()

			if len(alt_text.split('\n')) != 0:
				for i, text in enumerate(alt_text.split('\n')):
					# Index pertama pastikan tidak ada tanda dash
					if i == 0:
						# Single dash (-)
						cut_dash = text.split('-', 1)
						if len(cut_dash) == 2:
							text = cut_dash[1].strip()

						# Double dash (--)
						cut_double_dash = text.split('--', 1)
						if len(cut_double_dash) == 2:
							text = cut_double_dash[1].strip()

					if len(text) > 10:
						kompas_data.append(text)
			else:
				kompas_data.append(alt_text)

		# Jika list data ada maka pastikan tanda - atau -- dihilangkan
		else:
			split_1_dash = kompas_data[0].split('-', 1)
			split_2_dash = kompas_data[0].split('--', 1)

			# Cek split 1 dash
			if len(split_1_dash) == 2:
				kompas_data[0] = split_1_dash[1].strip()

			if len(split_2_dash) == 2:
				kompas_data[0] = split_2_dash[1].strip()

		return kompas_data

	else:
		return None


# noinspection PyShadowingNames
def extract_single_liputan6(liputan6_text_soup):
	print ("{Liputan6.com} single paged news")

	liputan6_data = []
	if liputan6_text_soup is not None:
			for tag in liputan6_text_soup.find_all(reversed=False):

				if tag.name == 'p':
					# Hapus pub signature (Liputan6.com)
					b_soup = tag.find('b')
					if b_soup is not None:
						if b_soup.text.lower().find('liputan6') != -1:
							print("{liputan6} Signature ditemukan dlm B: %s" % b_soup.text)
							b_soup.extract()

					# Memastikan string kosong dan teks skunder di skip
					# sehingga boleh masuk dalam list
					# cth: len("Baca juga") == 9 diskip.
					tag_text = tag.get_text().strip()
					if len(tag_text) > 10:
						liputan6_data.append(unidecode(tag_text))

	# bersihkan tanda dash pada index pertama.
	# liputan6_cuts = liputan6_data[0].split('-', 1)
	# if len(liputan6_cuts) == 2:
	# 	liputan6_data[0] = liputan6_cuts[1].strip()
	return liputan6_data


# noinspection PyShadowingNames
def get_paged_news_text(news_url):
	url_news_id = news_url.rsplit('/', 1)[0]
	url_news_data = news_url.rsplit('/', 1)[1]

	# Data yang akan dikembalikan
	# 1. Dict untuk untuk menampung data berita
	news_contents = {'news_title': "", 'news_content': "", 'news_image_hero': "", 'news_pub_date': None}
	# 2. List untuk menampung setiap paragraf atau kalimat dalam teks berita.
	news_data = []

	print ("Mulai manual news text parsing %s..." % news_url)

	# Inisialisasi Python Goose dengan exception
	try:
		goose_instance = Goose()
		article = goose_instance.extract(url=news_url)
	except IndexError as ie:
		print("ERROR! URL tidak bisa diproses. URL:%s\nMessage:%s" % (news_url, ie))
		return None

	# Soup untuk menampung seluruh dokumen HTML
	main_soup = BeautifulSoup(article.raw_html)

	# Pastikan judul berita hanya berupa unicode (Jan, 7th)
	news_contents['news_title'] = unidecode(article.title)

	# Mengambil gambar dan tanggal publikasi berita
	if article.top_image is not None:
		# Gambar dari hasil ekstaksi Goose
		news_contents['news_image_hero'] = article.top_image.src
	else:
		print("Grab image using Newspaper")
		newspaper_article = Article(url=news_url, language="id")
		newspaper_article.download()
		newspaper_article.parse()
		news_contents['news_image_hero'] = newspaper_article.top_image

	# Datetime dengan timezone
	# !!! Harus dalam lingkungan Django
	# timezone.activate(pytz.timezone("Asia/Jakarta"))
	# news_contents['news_pub_date'] = timezone.now()

	# LOGGING
	# print("News url: %s..." % news_url[:50])
	# print("Image url: %s..." % news_contents['news_image_hero'][:50])
	# print("News title: %s..." % news_contents['news_title'][:50])
	# print("News pub date: %s" % news_contents['news_pub_date'])

	# Soup untuk detik.com (dipanggil dari news_extractor.py)
	article_soup = None

	# memeriksa indikasi halaman bersambung
	# 1. Berita Kompas
	if "kompas" in news_url.split('.'):
		# Hilangkan tulisan "Kompas.com" pada judul
		news_contents['news_title'] = article.title.split('Kompas.com', 1)[0].strip()
		news_contents['news_title'] = article.title.rsplit('-', 1)[0].strip()

		# Berita bersambung
		kompas_soup = main_soup.find("div", class_="kcm-read-paging mt2")

		# Periksa apakah berita bersambung ada
		if kompas_soup is not None:
			news_data = extract_pagination_kompas(kompas_soup)
		else:
			# Mengambil berita utuh
			kompas_text_soup = main_soup.find('div', class_="kcm-read-text")
			news_data = extract_single_kompas(kompas_text_soup)
	# 2. Berita detik
	elif "detik" in news_url.split('.'):
		# Periksa apakah webpage detik merupakan berita terpisah-pisah (berita bersambung)
		article_soup = main_soup.find("div", class_="artikel2")
	# 3. Berita Liputan 6
	elif "liputan6" in news_url.split('.'):
		# Berita bersambung
		liputan6_soup = main_soup.find("section", class_="read-page--multi-page--pagination")
		if liputan6_soup is not None:
			news_data = extract_pagination_liputan6(liputan6_soup)
		else:
			liputan6_content_soup = main_soup.find("div", class_="read-page__content-body text-detail")
			news_data = extract_single_liputan6(liputan6_content_soup)

	# Proses berita detik yang bersambung
	# Dipanggil dari news_extractor.py
	# Karena detik mempunyai RSS Feed
	if article_soup is not None:
		detik_news_texts = []
		next_soup = article_soup.find("div", class_="multipage multipage2")

		# Save first data
		detik_data1 = extract_detik(article_soup)
		if len(detik_data1) != 0:
			for teks in detik_data1:
				detik_news_texts.append(teks)

		# Parsing total page from page
		total_news_page = 0
		for i, tag in enumerate(next_soup.find_all("span")):
			if tag.name == 'span':
				text = tag.get_text()
				if text.find("dari") != -1:
					print ("Current page: %s" % text)
					total_news_page = int(text.split('dari')[1])

		# Generate all next page URL
		print ("Detiks' total page: ", total_news_page)
		for i in range(total_news_page - 1):
			next_url = "%s/%d/%s" % (url_news_id, (i + 2), url_news_data)

			# Create goose instance
			next_goose_instance = Goose()
			next_article = next_goose_instance.extract(url=next_url)
			next_detik_soup = BeautifulSoup(next_article.raw_html)
			next_article_soup = next_detik_soup.find("div", class_="artikel2")

			# Save next data
			detik_data1 = extract_detik(next_article_soup)
			if len(detik_data1) != 0:
				for teks in detik_data1:
					detik_news_texts.append(teks)

			# Menghapus "Jakarta - " yang biasanya ada pada awal-awal list.
			if len(detik_news_texts) != 0:
				for i, teks in enumerate(detik_news_texts):
					if i == 0:
						if teks.find('-') != -1:
							detik_news_texts.pop(i)
					if i == 1:
						if teks.find('-') != -1:
							detik_news_texts.pop(i)
							detik_news_texts.pop(0)
						break

		news_data = detik_news_texts

	# News Content string isi berita
	if type(news_data) == list:
		news_text = '\n\n'.join(news_data)
		print(news_text)
		print(len(news_text))
		if len(news_text) > 500:
			news_contents['news_content'] = '\n\n'.join(news_data)
		else:
			return None
	else:
		print("Data is not a list")
		return None

	return news_contents


def parse_alexa_rank(alexa_url):
	# Inisialisasi Python Goose
	try:
		goose_alexa = Goose()
		alexa_article = goose_alexa.extract(url=alexa_url)
	except IndexError as ie:
		print("ERROR! URL tidak bisa diproses. URL:%s\nMessage:%s" % (alexa_url, ie))
		return None

	# Soup untuk menampung seluruh dokumen HTML
	alexa_main_soup = BeautifulSoup(alexa_article.raw_html)

	print(alexa_article.title)

	url_list = alexa_main_soup.find("div", class_="listings")

	if url_list is not None:
		# print(unidecode(url_list.prettify()))
		for i, a_tag in enumerate(url_list.find_all('p')):
			print("%.3d - %s" % ((i + 1), a_tag.get_text().strip()))
	else:
		print("URL tidak bisa diparsing.")


# Test fungsi pagnating_news
if __name__ == '__main__':
	# Detik
	# url = "http://health.detik.com/read/2015/12/23/201611/3103649/766/5-alasan-tidur-kelamaan-tidak-lebih-baik-dari-kurang-tidur"
	# url_single_page = "http://health.detik.com/read/2015/12/23/133023/3103206/1202/bertemu-taylor-swift-jadi-kado-natal-terindah-bagi-anak-dengan-kanker-ini"
	# url = "http://health.detik.com/read/2016/01/10/090117/3114600/764/hai-bunda-begini-cara-melatih-anak-agar-bisa-jadi-pendengar-yang-baik?l992205755"

	# Kompas
	# Single
	# url = "http://sains.kompas.com/read/2016/01/04/10502031/Teka-teki.Naskah.Kuno.di.Birmingham.Benarkah.Al.Quran.Pertama.di.Dunia."
	url = "http://tekno.kompas.com/read/2016/01/20/11581437/Ada.Apa.di.Balik.Penggratisan.WhatsApp."
	# Paged
	# url = "http://tekno.kompas.com/read/2015/07/26/11120087/Ini.5.Aplikasi.yang.Wajib.Dihapus.dari.Android"
	# url = "http://tekno.kompas.com/read/2015/12/30/13140077/Pengguna.Instagram.Berlomba.Pamer.9.Foto.Terbaik"
	# url = "http://ekonomi.kompas.com/read/2016/01/21/081537426/Faktor.Eksternal.jadi.Penggerak.Utama.Rupiah.Hari.Ini"
	# Liputan6
	# url = "http://health.liputan6.com/read/2396905/13-cara-sayangi-jantung"
	# url = "http://lifestyle.liputan6.com/read/2403246/punya-resolusi-lebih-banyak-baca-buku-ini-cara-mewujudkannya"

	# Test parse Alexa
	alexa_rank_url = "http://www.alexa.com/topsites/countries;1/ID"
	parse_alexa_rank(alexa_rank_url)

	news_contents = get_paged_news_text(url)
	if news_contents is not None:
		news_texts = news_contents['news_content']
		# print("News text:\n\"%s...%s\"" % (news_texts[:30], news_texts[-20:]))
		print("News text:\n\"%s\"" % news_texts)
	else:
		print("News content is empty")

	# Inisialisasi Python Goose
	# goose_instance = Goose()
	# article = goose_instance.extract(url='http://otomotif.kompas.com/')  # http://news.kompas.com akan gagal
	# main_soup = BeautifulSoup(article.raw_html)

	# urls = []
	# for tag in main_soup.find_all('a'):
	# 	if tag.get('href').find("otomotif.kompas.com/read") != -1:
	# 		urls.append(tag.get('href'))

	# url_set = list(set(urls))

	# for i, url in enumerate(url_set[:5]):
	# 	print("%d - %s" % (i, url))
