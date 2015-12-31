# coding=utf-8
from goose import Goose
from newspaper import Article

# Regular Expression utk membersihkan teks
import re

# Menangani karakter no ASCII
# from unidecode import unidecode

# Special case for detik tekno news
from bs4 import BeautifulSoup

# Kelola URL
from urlparse import urlparse

# Timing computation time
import timing

# Date time
from datetime import date

# Menangani karakter no ASCII
from unidecode import unidecode

# test_html = u'<span class="rcnt">8.668</span><span class="rcnt">5.7868</span>'


def extract_detik(article_soup):

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
					tag.strong.string += ". \n"
					tag.unwrap()
					continue
				tag.unwrap()
			tag.unwrap()
			print "Tag %s found" % tag.name

	# print u"\n\n%s\n" % article_soup.prettify()

	for string in article_soup.stripped_strings:
		print repr(string)

	# article_soup.find(attrs={"class": "leftside"}).extract()
	# print "HASIL:\n" , article_soup.prettify()

	return article_soup.get_text(' ', strip=True)


def extract_pagination_liputan6(liputan6_soup_data):
	liputan6_data = []
	liputan6_urls = []

	goose_instance = Goose()

	# Ambil url-url berita
	pagination_list_soup = liputan6_soup_data.find("ul", class_="read-page--multi-page--pagination__list")
	for tag in pagination_list_soup.find_all('a'):
		url_href = tag.get('href')
		liputan6_urls.append(url_href)

		# Memperoleh data dari internet
		article = goose_instance.extract(url=url_href)
		raw_html = article.raw_html
		liputan6_soup_data = BeautifulSoup(raw_html)

		# Ambil kontent
		liputan6_content_soup = liputan6_soup_data.find("div", class_="read-page__content-body text-detail")
		if liputan6_content_soup is not None:
			for tag in liputan6_content_soup.find_all(reversed=False):
				if tag.name == 'p':
					# print ("(%s)" % unidecode(tag.get_text()))
					liputan6_data.append(unidecode(tag.get_text()))

	# bersihkan tanda dash pada index pertama.
	liputan6_cuts = liputan6_data[0].split('-', 1)
	if len(liputan6_cuts) == 2:
		liputan6_data[0] = liputan6_cuts[1].strip()

	return liputan6_data


def extract_pagination_kompas(kompas_soup_data):
	kompas_data = []

	# Ambil URL "?page=all", untuk versi lengkap
	# berita
	single_page_url = None
	for tag in kompas_soup_data.find_all('a'):
		url_href = tag.get('href')
		if url_href.find("page=all") != -1:
			single_page_url = url_href
			break

	# Ambil data dari internet menggunkan URL Single Page
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

				if tag.name == 'p':
					# print ("(%s)" % unidecode(tag.get_text()))
					kompas_data.append(unidecode(tag.get_text()))
					tag.unwrap()

	# bersihkan tanda dash pada index pertama.
	kompas_cuts = kompas_data[0].split('--', 1)
	if len(kompas_cuts) == 2:
		kompas_data[0] = kompas_cuts[1].strip()

	return kompas_data


def extract_single_kompas(kompas_content_soup):
	kompas_data = []
	if kompas_content_soup is not None:

		for tag in kompas_content_soup.find_all(recursive=False):
			if tag.name == 'div':
				tag.extract()

			if tag.name == 'p':
				# print ("(%s)" % unidecode(tag.get_text()))
				kompas_data.append(unidecode(tag.get_text()))
				tag.unwrap()

		# bersihkan tanda dash pada index pertama.
		kompas_cuts = kompas_data[0].split('--', 1)
		if len(kompas_cuts) == 2:
			kompas_data[0] = kompas_cuts[1].strip()

		return kompas_data
	else:
		return None


def extract_single_liputan6(liputan6_text_soup):
	liputan6_data = []
	if liputan6_text_soup is not None:
			for tag in liputan6_text_soup.find_all(reversed=False):
				if tag.name == 'p':
					# print ("(%s)" % unidecode(tag.get_text()))
					liputan6_data.append(unidecode(tag.get_text()))

	# bersihkan tanda dash pada index pertama.
	liputan6_cuts = liputan6_data[0].split('-', 1)
	if len(liputan6_cuts) == 2:
		liputan6_data[0] = liputan6_cuts[1].strip()
	return liputan6_data


def get_paged_news_text(news_url):

	url_news_id = news_url.rsplit('/', 1)[0]
	url_news_data = news_url.rsplit('/', 1)[1]

	# Parse URL string
	o = urlparse(news_url)

	# This year
	this_year = date.today().year

	# Data yang akan dikembalikan
	# 1. Dict untuk untuk menampung data berita
	news_contents = {'news_title': "", 'news_content': "", 'news_image_hero': "", 'news_pub_date': None}
	# 2. List untuk menampung teks
	news_data = []

	goose_instance = Goose()
	article = goose_instance.extract(url=news_url)
	main_soup = BeautifulSoup(article.raw_html)

	news_contents['news_title'] = article.title

	# Mengambil gambar
	if article.top_image is not None:
		# Gambar dari hasil ekstaksi Goose
		news_contents['news_image_hero'] = article.top_image.src
	else:
		print("Grab image using Newspaper")
		newspaper_article = Article(url=news_url, language="id")
		newspaper_article.download()
		newspaper_article.parse()
		news_contents['news_image_hero'] = newspaper_article.top_image
		news_contents['news_pub_date'] = newspaper_article.publish_date

	print("Image url: %s" % news_contents['news_image_hero'])
	print("News title: %s" % news_contents['news_title'].split('-', 1)[0].strip())
	print("News pub date: %s" % news_contents['news_pub_date'])

	article_soup = None  # detik
	kompas_soup = None
	liputan6_soup = None
	# memeriksa indikasi halaman bersambung
	# 1. Berita Kompas
	if "kompas" in news_url.split('.'):
		print("Found kompas.com")
		# Hilangkan tulisan "Kompas.com" pada judul
		news_contents['news_title'] = article.title.split('-', 1)[0].strip()
		# Berita bersambung
		kompas_soup = main_soup.find("div", class_="kcm-read-paging mt2")
		if kompas_soup is not None:
			news_data = extract_pagination_kompas(kompas_soup)
		else:
			kompas_text_soup = main_soup.find('div', class_="kcm-read-text")
			news_data = extract_single_kompas(kompas_text_soup)
	# 2. Berita detik
	elif "detik" in news_url.split('.'):
		print("Found detik.com")
		# Periksa apakah webpage detik merupakan berita terpisah-pisah
		article_soup = main_soup.find("div", class_="artikel2")
	# 3. Berita Liputan 6
	elif "liputan6" in news_url.split('.'):
		print("Found liputan6.com")

		# Berita bersambung
		liputan6_soup = main_soup.find("section", class_="read-page--multi-page--pagination")
		if liputan6_soup is not None:
			news_data = extract_pagination_liputan6(liputan6_soup)
		else:
			liputan6_content_soup = main_soup.find("div", class_="read-page__content-body text-detail")
			news_data = extract_single_liputan6(liputan6_content_soup)

	# Mulai extract isi berita bersambung
	# Berita detik
	if article_soup is not None:
		detik_news_texts = []
		next_soup = article_soup.find("div", class_="multipage multipage2")

		# Save first data
		detik_news_texts.append(extract_detik(article_soup))

		# Parsing total page from page
		total_news_page = 0
		for i, tag in enumerate(next_soup.find_all("span")):
			if tag.name == 'span':
				text = tag.get_text()
				if text.find("dari") != -1:
					print "Current page: %s" % text
					total_news_page = int(text.split('dari')[1])

		# Generate all next page URL
		print "Total page: ", total_news_page
		for i in range(total_news_page-1):
			next_url = "%s/%d/%s" % (url_news_id, (i+2), url_news_data)

			# Create goose instance
			next_goose_instance = Goose()
			next_article = next_goose_instance.extract(url=next_url)
			next_detik_soup = BeautifulSoup(next_article.raw_html)
			next_article_soup = next_detik_soup.find("div", class_="artikel2")

			# Save first data
			detik_news_texts.append(extract_detik(next_article_soup))

		news_data = detik_news_texts

	else:
		print "URL: %s is a single paged news." % news_url

	# News Content string isi berita
	news_contents['news_content'] = '\n\n'.join(news_data)

	return news_contents


# Test fungsi pagnating_news
if __name__ == '__main__':
	# Detik
	# url = "http://health.detik.com/read/2015/12/23/201611/3103649/766/5-alasan-tidur-kelamaan-tidak-lebih-baik-dari-kurang-tidur"
	# url_single_page = "http://health.detik.com/read/2015/12/23/133023/3103206/1202/bertemu-taylor-swift-jadi-kado-natal-terindah-bagi-anak-dengan-kanker-ini"

	# Kompas
	# url = "http://tekno.kompas.com/read/2015/07/26/11120087/Ini.5.Aplikasi.yang.Wajib.Dihapus.dari.Android?utm_source=RD&utm_medium=box&utm_campaign=Kaitrd"

	# Liputan6
	url = "http://health.liputan6.com/read/2396905/13-cara-sayangi-jantung"

	news_con = get_paged_news_text(url)
	news_texts = news_con['news_content']
	print("News text:\n %s" % news_texts[:100])
