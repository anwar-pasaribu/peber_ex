# !/usr/bin/python
# -*- coding: utf-8 -*-
import nltk.data
import os


# menentukan log ditampilkan atau tidak
is_log = True


class Parser(object):
	def __init__(self):
		self.ideal = 20.0
		self.stopWords = self.getStopWords()  # Mendapatkan list stopword

	def getKeywords(self, text):
		"""
		Menentukan keyword pada teks yang diberikan. Terdiri dari proses:
		1. Menghapus pungtuasi pada teks.
		2. Memecah teks menjadi kata-kata.
		3. Menghapus stopword (Stopword dari penelitian Tala (2003).

		"""
		text = self.removePunctations(text)
		words = self.splitWords(text)
		words = self.removeStopWords(words)

		# Untuk membersihkan kata yang muncul beberapa kali.
		uniqueWords = list(set(words))

		if is_log: print ("Total words: %d" % len(words))
		if is_log: print("Unique word count: %d" % len(uniqueWords))

		# Keywords merupakan dict yg berisi kata dan jumlah berapa kali muncul.
		keywords = [{'word': word, 'count': words.count(word)} for word in uniqueWords]

		# Keyword diurutkan decara Descending (Z-A)
		keywords = sorted(keywords, key=lambda x: -x['count'])

		return (keywords, len(words))

	def getSentenceLengthScore(self, sentence):
		# Ideal = 20.0
		# (20 - abs(20 - banyak_kata)) / 20
		if is_log: print "getSentenceLengthScore: (20.0 - abs(20.0 - %d) ) / 20.0 = %f" % \
		                 (len(sentence), ((self.ideal - abs(self.ideal - len(sentence))) / self.ideal))

		return (self.ideal - abs(self.ideal - len(sentence))) / self.ideal

	# Jagadeesh, J., Pingali, P., & Varma, V. (2005).
	# Sentence Extraction Based Single Document Summarization.
	# International Institute of Information Technology, Hyderabad, India, 5.
	def getSentencePositionScore(self, i, sentenceCount):
		# sentenceCount = Jumlah kalimat
		normalized = i / (sentenceCount * 1.0)
		if is_log: print "getSentencePositionScore: %d / (%d * 1.0) = %f " % (i, sentenceCount, normalized)

		if normalized > 0 and normalized <= 0.1:
			return 0.17
		elif normalized > 0.1 and normalized <= 0.2:
			return 0.23
		elif normalized > 0.2 and normalized <= 0.3:
			return 0.14
		elif normalized > 0.3 and normalized <= 0.4:
			return 0.08
		elif normalized > 0.4 and normalized <= 0.5:
			return 0.05
		elif normalized > 0.5 and normalized <= 0.6:
			return 0.04
		elif normalized > 0.6 and normalized <= 0.7:
			return 0.06
		elif normalized > 0.7 and normalized <= 0.8:
			return 0.04
		elif normalized > 0.8 and normalized <= 0.9:
			return 0.04
		elif normalized > 0.9 and normalized <= 1.0:
			return 0.15
		else:
			return 0

	def getTitleScore(self, title, sentence):
		titleWords = self.removeStopWords(title)
		sentenceWords = self.removeStopWords(sentence)

		# Mengambil kata-kata dalam kalimat yang sama dengan judul
		matchedWords = [word for word in sentenceWords if word in titleWords]

		if is_log: print "Title words: %s" % titleWords
		if is_log: print "Sentence words: %s" % sentenceWords
		if is_log: print "Matched words: %s" % matchedWords

		# Kembalikan (jumlah kata yg sama dengan judul) / (jumlah judul * 1)
		if is_log: print "Get title score: %d / %d * 1.0 = %f " % (
		len(matchedWords), len(titleWords), (len(matchedWords) / (len(titleWords) * 1.0)))

		return len(matchedWords) / (len(titleWords) * 1.0)

		# Memisahkan kalimat dengan NTLK Tokenizer.

	def splitSentences(self, text):
		tokenizer = nltk.data.load('nltk:tokenizers/punkt/english.pickle')  # Edited, mengambil dari d:nltk_daa
		return tokenizer.tokenize(text)

		# Pecahkan kalimat berita dan buat lower case

	def splitWords(self, sentence):
		return sentence.lower().split()

		# Menghilangkan tanda baca ! ? dsb

	def removePunctations(self, text):
		return ''.join(t for t in text if t.isalnum() or t == ' ')

	def removeStopWords(self, words):
		return [word for word in words if word not in self.stopWords]

	def getStopWords(self):
		with open(os.path.dirname(
				os.path.abspath(__file__)) + '/trainer/stopword_list_tala.txt') as file:  # Ganti ke stopwors Tala
			words = file.readlines()

		return [word.replace('\n', '') for word in words]
