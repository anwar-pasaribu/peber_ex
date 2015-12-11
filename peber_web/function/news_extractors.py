# coding=utf-8
"""
Fungsi untuk mengmabil isi berita dari URL berita.
"""
from goose import Goose
from newspaper import Article

# Regular Expression utk membersihkan teks
import re

# Menangani karakter no ASCII
from unidecode import unidecode

# Special case for detik tekno news
from BeautifulSoup import BeautifulSoup


class NewsExtractor(object):
	"""
	Kelas untuk ekstrak berita dari url yang dberikan.
	"""
	def __init__(self, feed_data_length, extracted_feed, news_corp_id, url):

		# Indikasi berita yg selesai diekstrak
		self.feed_data_length = feed_data_length  # Total feed yg akan diekstrak.
		self.extracted_feed = extracted_feed  # Jumlah feed yg selesai diekstrak

		self.news_corp_id = news_corp_id  # Untuk menentukan format teks
		self.url = url
		self.news_top_image = ""

		# Special case (Detik Tekno)
		self.detik_tekno_id = 20

		goose_instance = Goose()
		self.article = goose_instance.extract(url=url)

	def get_news_content(self):
		"""
		Memperoleh teks berita yang sudah di ekstrak
		:return: String teks berita
		"""
		text_length = len(self.article.cleaned_text)
		min_news_content = 500  # Peraturan teks berita harus besar minimum 500 huruf.

		# Ambil data secara manual dengan BeautifulSoup utk detik tekno.
		# DS - Detik Spesial
		if self.news_corp_id is self.detik_tekno_id:
			print("[|DS|] Data (%d of %d) get content, URL: %s" % (self.extracted_feed, self.feed_data_length, self.url))

			detik_soup = BeautifulSoup(self.article.raw_html)
			detik_soup_texts = detik_soup.find("div", {"class": "text_detail"})

			if detik_soup_texts is not None:
				# Tes banyak karakter dalam teks berita.
				if len(detik_soup_texts.text) > min_news_content:
					# Ambil teks dari soup dan hilangkan S:AUTHOR (paling bawah)
					detik_soup_texts = detik_soup_texts.text.split('S:AUTHOR', 1)[0]
					return format_news_content_texts(self.news_corp_id, detik_soup_texts)

		# Teks dari Goose
		if self.article.cleaned_text is not '' and text_length > min_news_content:
			print('Data (%d of %d) Using Goose. URL: %s' % (self.extracted_feed, self.feed_data_length, self.url))
			return format_news_content_texts(self.news_corp_id, self.article.cleaned_text)

		# Teks dari Newspaper
		else:
			article = Article(url=self.url, language="id")  # CNN Edition diabaikan.
			article.download()
			article.parse()
			self.news_top_image = article.top_image  # Simpan gambar berita jika parsing goose gagal

			print('Data (%d of %d) Using Newspaper. URL: %s' % (self.extracted_feed, self.feed_data_length, self.url))

			# Teks artikel harus > 500 karakter
			if len(article.text) > min_news_content:
				return format_news_content_texts(self.news_corp_id, article.text)
			else:
				# Kondisi terakhir, kembalikan None jika tidak ada kontent berita.
				return None

	def get_news_image_hero(self):
		"""
		Mendapatkan gambar utama berita
		:return: String url gambar berita
		"""
		if self.article.top_image is not None:
			# Gambar dari hasil ekstaksi Goose
			return self.article.top_image.src
		else:
			return self.news_top_image  # Hasil parsing Newspaper


def format_news_content_texts(news_corp_id, texts, delimiter='\n'):
	"""
	Format text berita supaya lebih bersih, tanpa banyak karakter '\n'
	:param texts: String teks berita yang akan dibersihkan
	:param news_corp_id: Id berita yg akan di olah
	:param delimiter: Pembatas setiap "paragraf"
	:return: Teks berita dalam format unicode.
	"""
	tempo_co_ids = [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]  # ID sumber berita tempo
	antara_news_ids = [43, 44, 45, 46, 47, 48, 49, 50]  # ID ANTARA News
	okezone_ids = [42, 41, 40, 39, 38, 37, 36, 19]
	tribun_ids = [22]  # Tribun Mixed (All Category)
	detik_ids = [35, 34, 33, 32, 31, 30, 20]
	repulika_ids = [77]
	metrotvnews_ids = [65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76]
	jpnn_ids = [78, 79, 80, 81, 82, 83, 84]

	# Hilangkan karakter non-ASCII (Stackoverflow)
	# Teks yg sudah di encode("utf-8")
	# my_texts = re.sub(r'[^\x00-\x7f]', r'', texts)  # Non aktif mulai (Nov 12)
	my_texts = unidecode(texts)

	# Ubah karakter hypen (em dan en) ke normal
	my_texts = my_texts.replace(u'--', '-')

	# Ubah setiap karakter titik setelahnya spasi.
	my_texts = my_texts.replace(u'.', '. ')

	# Proses awal untuk hilangkan caption foto atau "Baca Juga"
	# Pecahkan string isi berita menjadi array
	sentences = my_texts.split("\n")

	# hapus array yang bukan sebuah kalimat, lebih kecil dari 60 huruf
	# JPNN filter: 'BACA:' not in s and 'Foto:' not in s
	data = [s for s in sentences if len(s) > 60 and 'BACA:' not in s and 'Foto:' not in s and 'FOTO' not in s]
	my_texts = ""  # Buat lagi my_texts versi lebih bersih
	for s in data:
		my_texts = '%s%s\n' % (my_texts, s.strip())

	# Tempo; dua kriteria pemotongan
	if news_corp_id in tempo_co_ids:
		texts_cut_1 = re.split(r'TEMPO.[A-Z, ]+-?', my_texts, 1)

		if len(texts_cut_1) != 2:
			texts_cut_2 = my_texts.split('KOMUNIKA', 1)
			if len(texts_cut_2) == 2:
				my_texts = texts_cut_2[1].split(r'-', 1)[1].strip()
				my_texts = my_texts.rsplit("Baca juga:", 1)[0]  # Pecah lagi jika ada
		else:
			my_texts = texts_cut_1[1].split(r'-', 1)[1].strip()
			if len(my_texts) == 2:
				my_texts = my_texts[1].strip()
				my_texts = my_texts.rsplit("Baca juga:", 1)[0]  # Pecah lagi jika ada, index 0 akan selalu ada

	# Antara News
	elif news_corp_id in antara_news_ids:
		texts_cut_1 = re.split(r'ANTARA New[a-z]+\)? - ', my_texts, 1)  # re.split(" +", str1)
		if len(texts_cut_1) == 2:
			my_texts = texts_cut_1[1].rsplit('Editor:', 1)[0].strip()

	# Tribun News (Mixed)
	elif news_corp_id in tribun_ids:
		texts_cut_1 = re.split(r'-', my_texts, 1)
		if len(texts_cut_1) == 2:
			my_texts = texts_cut_1[1].strip()

	# Okezone
	elif news_corp_id in okezone_ids:
		texts_cut_1 = re.split(r'^[A-Z]{3,25} ?-? ?', my_texts, 1)  # Pisahkan dari "KOTA - " chars
		if len(texts_cut_1) == 2:
			texts_cut_2 = re.split(r'^[A-Z]{4,25} ?-? ?', texts_cut_1[1], 1)  # kasus NEW MEXICO
			if len(texts_cut_2) == 2:
				my_texts = texts_cut_2[1].strip()
			else:
				my_texts = texts_cut_1[1].strip()

	# Detik.com
	elif news_corp_id in detik_ids:
		texts_cut_1 = re.split(r'-', my_texts, 1)  # Belum tahu pola beritanya!
		if len(texts_cut_1) == 2:
			my_texts = texts_cut_1[1].strip()

	# Republika.co.id
	elif news_corp_id in repulika_ids:
		texts_cut_1 = re.split(r'REPUBLIKA. ?CO. ?ID, ?[A-Z ]+ ?-? ?', my_texts, 1)  # Pisahkan REPUBLIKA.CO.ID, PARIS -
		if len(texts_cut_1) == 2:
			my_texts = texts_cut_1[1].strip()

	# MetroTVNews.com
	elif news_corp_id in metrotvnews_ids:
		# Keriteria pemotongan pertama
		texts_cut_1 = re.split(r'[0-9]+ ?wib?', my_texts, 1)  # 19:08 wib : <Teks mulai>
		if len(texts_cut_1) == 2:
			texts_cut_2 = re.split(r'^:', texts_cut_1[1].strip(), 1)  # Hilangkan :
			if len(texts_cut_2) == 2:
				my_texts = texts_cut_2[1].strip()
			else:
				my_texts = texts_cut_1[1].strip()
		else:
			# Keriteria pemotongan kedua
			# Kata yang dimulai dengan "Metrotvnews..:"
			texts_cut_3 = re.split(r'Metrotvnews[a-zA-Z., ]+:?', my_texts, 1)
			if len(texts_cut_3) == 2:
				my_texts = texts_cut_3[1].strip()

	# JPNN News
	elif news_corp_id in jpnn_ids:
		texts_cut_1 = re.split(r'^[A-Za-z. ]{3,25} ?- ?', my_texts, 1)  # Pisahkan dari "KOTA - " chars
		if len(texts_cut_1) == 2:
			texts_cut_2 = texts_cut_1[1].rsplit('(', 1)  # Potong lagi dengan inisial penulis.
			if len(texts_cut_2) == 2:
				my_texts = texts_cut_2[0].strip()
			else:
				my_texts = texts_cut_1[1].strip()

	# Post Proses format teks
	# Pecahkan string isi berita menjadi array
	sentences = my_texts.split("\n")

	# hapus array yang bukan sebuah kalimat, lebih kecil dari 60 huruf
	data = [s for s in sentences]
	teks = ""  # teks penampung data yg akan dikirim

	for i in range(len(data)):
		if i == (len(data) - 1):  # Atur format akhir perulangan
			teks += data[i].strip()  # Tanpa tanda delimiter pada akhir kalimat
		else:
			# tambah string delimiter pada setiap akhir string
			teks = '{0}{1}{2}'.format(teks, data[i].strip(), delimiter)

	print("Selesai ekstrak teks id: %d" % news_corp_id)
	return u'{0}'.format(teks)
