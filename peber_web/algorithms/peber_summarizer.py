# coding=utf-8
"""
Kelas algoritma peringkasan. Algoritma yg digunakan:
1. Berasal dari repo github (pebahasa)
2. TextTeaser oleh Mojo Jolo Balbin
"""
from peber_web.pebahasa.summary import *
from .textteaser import TextTeaser
from gensim.summarization import summarize as gensim_summarize


class PeberSummarizer(object):
	"""
	Algoritma yg digunakan untuk meringkas.
	"""
	def __init__(self, text):
		self.text = text

	def pebahasa_summarizer(self):
		"""
		Algoritma dari repositor pebahasa.
		:return: String teks berita yang sudah diringkas
		"""
		try:
			return make_summary(self.text.replace('.', '. '))  # Masalah setelah titik harus spasi.
		except UnicodeTranslateError as e:
			return u'Unicode Error: {a}'.format(a=e, )

	def text_teaser_summarizer(self, news_title):
		"""
		Algoritma TextTeaser
		:param news_title: Judul berita yang akan disingkat
		:return: teks ringkasan dengan delimiter '\n'
		"""

		# Masalah setelah titik harus spasi.
		text_to_summarize = self.text.replace('.', '. ')

		text_teaser = TextTeaser()
		sentences = text_teaser.summarize(news_title, text_to_summarize)

		# Kalimat hasil ringkasan dipisahkan \n 
		summarized = ""
		for text in sentences:
			summarized += '{0}\n'.format(text)

		return u'{0}'.format(summarized)

	def gensim_bm25_summarizer(self):
		"""
		Algoritma BM25 Ranking Function.
		:return: Summarized Text.
		"""

		# Masalah setelah titik harus spasi.
		text_to_summarize = self.text.replace('.', '. ')
		
		return u'{0}'.format(gensim_summarize(text_to_summarize))

