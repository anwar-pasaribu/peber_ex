# coding=utf-8
from .textteaser import TextTeaser
from .sumy.parsers.plaintext import PlaintextParser
from .sumy.nlp.tokenizers import Tokenizer
from .sumy.summarizers.lex_rank import LexRankSummarizer as LexRankSummarizer
from .sumy.summarizers.lsa import LsaSummarizer as LSASummarizer
from .sumy.summarizers.text_rank import TextRankSummarizer as TextRankSummarizer
from .sumy.nlp.stemmers import Stemmer
from .sumy.utils import get_stop_words

import re


LANGUAGE = "english"
SENTENCES_COUNT = 5


"""
Kelas algoritma peringkasan. Algoritma yg digunakan:
1. A1 - LexRank Algorithm
2. A2 - LSA Algorithm
3. A3 - TexRank Algorithm
"""


class PeberSummarizer(object):
	"""
	Algoritma yg digunakan untuk meringkas.
	"""
	def __init__(self, text):
		self.text = text

	def clean_texts(self):
		"""
		Membersihkan teks berita atau memperbaiki format
		"""
		# Masalah setelah titik harus spasi.
		# Hal ini berguna untuk memastikan tidak ada yang menyatu dengan titik,
		# seperti kalimat1.kalimat2 (kedua kalimat bersatu). Kemudian begitu juga
		# untuk tanda tanya (?).
		c_text = self.text.replace('.', '. ')
		c_text = c_text.replace(' ?', '? ')

		# Updated Jan 7th.
		# Kemudian pada kasus 999. 999. Nomor harus tetap disatukan dengan titik
		# menjadi 999.999. Kemudian untuk kasus "kalimat 999. New_kalimat" akan dibiarkan.
		matched_regex = re.findall("[-+]?\d+[\.] \d+", c_text)
		if len(matched_regex) != 0:
			for found in matched_regex:
				c_text = c_text.replace(found, found.replace(' ', ''))
		return c_text

	def text_teaser_summarizer(self, news_title):
		"""
		Algoritma TextTeaser (Balbino, 2011)
		:param news_title: Judul berita yang akan disingkat
		:return: Teks ringkasan dengan delimiter '\n'
		"""
		# Masalah setelah titik harus spasi.
		# Hal ini berguna untuk memastikan tidak ada yang menyatu dengan titik,
		# seperti kalimat1.kalimat2 (kedua kalimat bersatu). Kemudian begitu juga
		# untuk tanda tanya (?).
		text_to_summarize = self.text.replace('.', '. ')
		text_to_summarize = text_to_summarize.replace(' ?', '? ')

		# Updated Jan 7th.
		# Kemudian pada kasus 999. 999. Nomor harus tetap disatukan dengan titik 
		# menjadi 999.999. Kemudian untuk kasus "kalimat 999. New_kalimat" akan dibiarkan.
		matched_regex = re.findall("[-+]?\d+[\.] \d+", text_to_summarize)
		if len(matched_regex) != 0:
			for found in matched_regex:
				text_to_summarize = text_to_summarize.replace(found, found.replace(' ', ''))

		text_teaser = TextTeaser()
		sentences = text_teaser.summarize(news_title, text_to_summarize)

		# Kalimat hasil ringkasan dipisahkan \n 
		summarized = ""
		for text in sentences:
			summarized += '{0}\n\n'.format(text)  # Tambah dua line (Des, 20th)

		return u'{0}'.format(summarized)

	def lex_rank_summarizer(self):
		"""
		Algoritma pertama:
		LexRank
		"""
		text_to_summarize = self.clean_texts()

		parser = PlaintextParser.from_string(text_to_summarize, Tokenizer(LANGUAGE))
		stemmer = Stemmer(LANGUAGE)
		summarizer = LexRankSummarizer(stemmer)
		summarizer.stop_words = get_stop_words('indonesia')
		sentences = ""
		for sentence in summarizer(parser.document, SENTENCES_COUNT):
			sentences = "%s\n\n%s" % (sentences, sentence)
		# print(sentence)

		return sentences

	def lsa_summarizer(self):
		"""
		Algoritma pertama:
		LSA
		"""
		text_to_summarize = self.clean_texts()

		parser = PlaintextParser.from_string(text_to_summarize, Tokenizer(LANGUAGE))
		stemmer = Stemmer(LANGUAGE)
		summarizer = LSASummarizer(stemmer)
		summarizer.stop_words = get_stop_words('indonesia')
		sentences = ""
		for sentence in summarizer(parser.document, SENTENCES_COUNT):
			sentences = "%s\n\n%s" % (sentences, sentence)
		# print(sentence)

		return sentences

	def text_rank_summarizer(self):
		"""
		Algoritma yang akan menjadi referensi untuk evaluasi hasil ringkasan
		TextTeaser.
		:return: Teks hasil ringkasan.
		"""
		# Format teks sehingga pemisah antar kalimat lebih rapih.
		text_to_summarize = self.clean_texts()

		parser = PlaintextParser.from_string(text_to_summarize, Tokenizer(LANGUAGE))
		stemmer = Stemmer(LANGUAGE)
		summarizer = TextRankSummarizer(stemmer)
		summarizer.stop_words = get_stop_words('indonesia')
		sentences = ""
		for sentence in summarizer(parser.document, SENTENCES_COUNT):
			sentences = "%s\n\n%s" % (sentences, sentence)
			# print(sentence)

		return sentences
