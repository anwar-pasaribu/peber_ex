# coding=utf-8
# Untuk menyimpan data ke database
from dateutil.parser import parse

# Model
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from ..models import News, News_Source

# Ekstrak info from
from news_extractors import NewsExtractor

# Import algoritma peringkas
from peber_web.algorithms.peber_summarizer import PeberSummarizer
from sumy.evaluation.coselection import f_score
from sumy.evaluation.coselection import precision
from sumy.evaluation.coselection import recall


class DatabaseAccess(object):
	def __init__(self):
		self.language = "english"

	def insert_news_data(self, data):
		"""
		Insert data to news table.
		:return Jumlah data yang baru dibuat.
		"""

		new_data_count = 0
		feed_data_length = len(data.entries)
		extracted_feed = 0

		# Jika berhasil ambil dar RSS Fedd
		for post in data.entries:

			# Deklarasi var untuk data berita.
			news_url = post.guid
			news_title = post.title
			news_content = None
			# news_corp = None
			news_summary = None
			news_text_rank_summary = None
			val_f_score = 0
			val_precision = 0
			val_recall = 0
			news_pub_date = parse(post.published)
			news_image_hero = None

			# Cek jika URL merupakan link untuk foto galeri.
			# Kasus untuk URL Foto Galeri Detik.com. (2 Des)
			gallery_url = 'readfoto' in news_url.split('/')
			if gallery_url:
				print("URL berita galeri (readfoto), proses dilewatkan.")
				continue

			# Status keberadaan data dalam database.
			is_data_available = News.objects.filter(news_url=news_url).exists()

			# Periksa apakah data sudah ada dalam database
			if not is_data_available:
				# Tambah Info total berita dan berapa yang selesai diekstrak.
				g = NewsExtractor(feed_data_length, extracted_feed, data.news_corp_id, news_url)
				news_content = g.get_news_content()
				news_image_hero = g.get_news_image_hero()

				# News Summary dengan Text Teaser dan Text Rank
				# Jika konten berita tidak None
				if news_content is not None:
					peber_summ = PeberSummarizer(news_content)
					news_summary = peber_summ.text_teaser_summarizer(news_title)
					news_text_rank_summary = peber_summ.lex_rank_summarizer()

					# Mulai Menghitung F/P/R
					reference_summary = news_text_rank_summary
					evaluated_summ = news_summary

					# Menghitung score
					reference_document = PlaintextParser.from_string(reference_summary, Tokenizer(self.language))
					reference_sentences = reference_document.document.sentences

					evaluated_doc = PlaintextParser.from_string(evaluated_summ, Tokenizer(self.language))
					evaluated_sent = evaluated_doc.document.sentences

					val_f_score = f_score(evaluated_sent, reference_sentences)
					val_precision = precision(evaluated_sent, reference_sentences)
					val_recall = recall(evaluated_sent, reference_sentences)

					print("Meringkas: %s selesai." % news_title)				

			# Periksa apakah konten berita hasil ekstraksi dan hasil ringkasan ada
			if news_content and news_summary is not None:

				new_news = News(
					news_url=news_url,
					news_title=news_title,
					news_content=news_content,
					news_summary=news_summary,
					news_text_rank_summary=news_text_rank_summary,
					f_score=val_f_score,
					precision=val_precision,
					recall=val_recall,
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

	def insert_news_to_db(self, news_data):
		"""
		Memasukkan data berita ke dalam database.
		:param news_data: Dictionary berisi konten berita.
		:return: ID berita yang berhasil dimasukkan ke dalam database.
		"""

		# Deklarasi var untuk data berita.
		news_url = news_data['news_url']
		news_corp = news_data['news_corp']
		news_pub_date = news_data['news_pub_date']

		news_title = news_data['news_title']
		news_content = news_data['news_content']
		news_image_hero = news_data['news_image_hero']

		# Inisialisasi kelas untuk
		peber_summ = PeberSummarizer(news_content)
		news_summary = peber_summ.text_teaser_summarizer(news_title)
		news_text_rank_summary = peber_summ.lex_rank_summarizer()

		# Mulai Menghitung F/P/R
		reference_summary = news_text_rank_summary
		evaluated_summ = news_summary

		# Menghitung score
		reference_document = PlaintextParser.from_string(reference_summary, Tokenizer(self.language))
		reference_sentences = reference_document.document.sentences

		evaluated_doc = PlaintextParser.from_string(evaluated_summ, Tokenizer(self.language))
		evaluated_sent = evaluated_doc.document.sentences

		val_f_score = f_score(evaluated_sent, reference_sentences)
		val_precision = precision(evaluated_sent, reference_sentences)
		val_recall = recall(evaluated_sent, reference_sentences)

		new_news = News(
			news_url=news_url,
			news_title=news_title,
			news_content=news_content,
			news_summary=news_summary,
			news_text_rank_summary=news_text_rank_summary,
			f_score=val_f_score,
			precision=val_precision,
			recall=val_recall,
			news_pub_date=news_pub_date,
			news_image_hero=news_image_hero
		)

		new_news.news_corp_id = news_corp  # Menentukan publisher
		new_news.save()  # Menyimpan data berita

		# Jika id yg dikembalikan tidak 0
		# berarti penyimpanan berhasil
		if new_news.id is not 0:
			return new_news.id
		else:
			return 0

	def get_all_news_source(self):
		self.__init__()
		return News_Source.objects.all()

	def get_all_news(self):
		self.__init__()
		return News.objects.all()
