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
from peber_web.function.paginating_news import get_paged_news_text


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

		# Inisialisasi Python Goose dengan exception (Feb 9)
		try:
			goose_instance = Goose()
			self.article = goose_instance.extract(url=url)
		except IndexError as ie:
			self.article = None
			print("ERROR! URL tidak bisa diproses. URL:%s\nMessage:%s" % (url, ie))

	def get_news_content(self):
		"""
		Memperoleh teks berita yang sudah di ekstrak
		:return: String teks berita
		"""
		# Kasus URL tidak bisa diparse
		if self.article is None:
			return None

		text_length = len(self.article.cleaned_text)
		min_news_content = 500  # Peraturan teks berita harus besar minimum 500 huruf.

		# Special case for detik.com, jika halaman berita bersambung
		# akan di proses menggunakan fungsi get_paged_news_text()
		detik_ids = [35, 34, 33, 32, 31, 30, 20]
		if self.news_corp_id in detik_ids:
			print("{detik} Data (%d of %d) get content, URL: %s" % (self.extracted_feed, self.feed_data_length, self.url))
			detik_soup = BeautifulSoup(self.article.raw_html)
			next_soup = detik_soup.find("div", class_="multipage multipage2")

			if next_soup is not None:
				news_contents = get_paged_news_text(self.url)
				return format_news_content_texts(self.news_corp_id, news_contents['news_content'])

		# Teks dari Goose
		if self.article.cleaned_text is not '' and text_length > min_news_content:
			print('Data (%d of %d) Using Goose. URL: %s' % (self.extracted_feed, self.feed_data_length, self.url))
			return format_news_content_texts(self.news_corp_id, self.article.cleaned_text)
		# Teks dari Newspaper
		else:
			article = Article(url=self.url, language="id")
			article.download()
			article.parse()
			self.news_top_image = article.top_image  # Simpan gambar berita jika parsing goose gagal

			print('Data (%d of %d) Using Newspaper. URL: %s' % (self.extracted_feed, self.feed_data_length, self.url))

			# Teks artikel harus > 500 karakter
			if article.text is not None and len(article.text) > min_news_content:
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


def format_news_content_texts(news_corp_id, texts, delimiter='\n\n'):  # Add two delimiters (Des, 18th) 
	"""
	Format text berita supaya lebih bersih, tanpa banyak karakter '\n'
	:param texts: String teks berita yang akan dibersihkan
	:param news_corp_id: Id berita yg akan di olah
	:param delimiter: Pembatas setiap "paragraf"
	:return: Teks berita dalam format unicode.
	"""
	detik_ids = [35, 34, 33, 32, 31, 30, 20]  # 33: Detik Health

	# Hilangkan karakter non-ASCII (Stackoverflow)
	# Teks yg sudah di encode("utf-8")
	# my_texts = re.sub(r'[^\x00-\x7f]', r'', texts)  # Non aktif mulai (Nov 12)
	my_texts = unidecode(texts)

	# Ubah karakter hypen (em dan en) ke normal
	my_texts = my_texts.replace(u'--', '-')

	# Proses awal untuk hilangkan caption foto atau "Baca Juga"
	# Pecahkan string isi berita menjadi array
	sentences = my_texts.split("\n")

	# Hapus array yang bukan sebuah kalimat, lebih kecil dari 10 huruf
	# JPNN filter: 'BACA:' not in s and 'Foto:' not in s
	data = [s for s in sentences if len(s) > 10 and 'BACA:' not in s and 'Foto:' not in s and 'FOTO' not in s]
	my_texts = ""  # Buat lagi my_texts versi lebih bersih
	for s in data:
		my_texts = '%s%s\n' % (my_texts, s.strip())

	# TODO Pemotongan berita Detik.com
	if news_corp_id in detik_ids:
		texts_cut_1 = re.split(r'@@@', my_texts, 1)  # Belum tahu pola beritanya!
		if len(texts_cut_1) == 2:
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

	# print("Selesai ekstrak teks id: %d" % news_corp_id)
	return u'{0}'.format(teks)
