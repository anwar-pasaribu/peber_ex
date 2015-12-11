# coding=utf-8
# Untuk menyimpan data ke database
from dateutil.parser import parse

# Model
from ..models import News, News_Source

# Ekstrak info from
from news_extractors import NewsExtractor

# Import algoritma peringkas
from peber_web.algorithms.textteaser import TextTeaser


class DatabaseAccess(object):
	def __init__(self):
		pass

	def insert_news_data(self, data):
		"""
		Insert data to news table.
		:return Jumlah data yang baru dibuat.
		"""

		new_data_count = 0
		feed_data_length = len(data.entries)
		extracted_feed = 0

		for post in data.entries:

			# Deklarasi var untuk data berita.
			news_url = post.guid
			news_title = post.title
			news_content = ""
			# news_corp = None
			news_summary = "N/A"
			news_pub_date = parse(post.published)
			news_image_hero = ""

			# Hapus JPNN.com 
			news_title = news_title.replace('-JPNN.com', '')

			# Cek jika URL merupakan link untuk foto galeri.
			# Kasus untuk URL Foto Galeri Detik.com. (2 Des)
			gallery_url = 'readfoto' in news_url.split('/')

			# Status keberadaan data dalam database.
			is_data_available = News.objects.filter(news_url=news_url, news_title=news_title).exists()

			# Jika bukan url foto galeri dan belum ada di database
			if not gallery_url and not is_data_available:
				# Tambah Info total berita dan berapa yang selesai diekstrak.
				g = NewsExtractor(feed_data_length, extracted_feed, data.news_corp_id, news_url)
				news_content = g.get_news_content()
				news_image_hero = g.get_news_image_hero()

				# News Summary dengan Text Teaser 
				# Jika konten berita tidak None
				if news_content is not None:
					text_teaser = TextTeaser()
					sentences = text_teaser.summarize(news_title, news_content)

					# Kalimat hasil ringkasan dipisahkan \n
					summarized = ""
					for text in sentences:
						summarized += '{0}\n'.format(text)

					news_summary = summarized
					print("Meringkas: %s selesai." % news_title)

			# Periksa apakah data sudah ada, jika ada tidak jadi simpan data lagi.
			# Kemudian konten berita tidak None.
			if not is_data_available and news_content is not None:

				new_news = News(
					news_url=news_url,
					news_title=news_title,
					news_content=news_content,
					news_summary=news_summary,
					news_pub_date=news_pub_date,
					news_image_hero=news_image_hero
				)

				new_news.news_corp_id = data.news_corp_id  # Menentukan publisher
				new_news.save()  # Menyimpan data berita

				# Jika id yg dikembalikan tidak 0
				# berarti penyimpanan berhasil
				if new_news.id is not 0:
					new_data_count += 1
					extracted_feed += 1  # Increment indikasi data terektrak
				else:
					print("Gagal menyimpan %s ke database" % news_title)

			else:
				print("Berita sudah ada atau teks (None). Judul: %s" % news_title)

		return new_data_count

	def get_all_news_source(self):
		return News_Source.objects.all()

	def get_all_news(self):
		return News.objects.all()
