#!/usr/bin/python
# -*- coding: utf-8 -*-
from .parser import Parser
from pprint import pprint

# menentukan log ditampilkan atau tidak
is_log = True


class Summarizer(object):
	def __init__(self):
		self.parser = Parser()

	def summarize(self, text, title, source, category):

		# Preprocessing
		# 1. Memisahkan teks berita menjadi kalimat menggunakan NLTK Sentence Tokenizer.
		sentences = self.parser.splitSentences(text)
		# 2. Menghapus tanda baca pada judul
		titleWords = self.parser.removePunctations(title)
		# 3. Memisahkan judul berita menjadi kata-kata berdasarkan tanda sapasi.
		titleWords = self.parser.splitWords(titleWords)

		# Bagian untuk hapus stopword
		# Params:
		# wordCount = banyak semua kata dalam teks
		# keywords = Kata dana jumlah dalam dictionary
		(keywords, wordCount) = self.parser.getKeywords(text)

		# Mengambil 10 top keyword paling sering muncul
		if is_log:
			print("Before keyworded:")
			pprint(keywords[:10])
		topKeywords = self.getTopKeywords(keywords[:10], wordCount, source, category)
		if is_log:
			print("After Topkeywords:")
			pprint(topKeywords)

		result = self.computeScore(sentences, titleWords, topKeywords)
		if is_log:
			print("Compute Score Result:")
			pprint(result)

		result = self.sortScore(result)
		if is_log:
			print "Sort Score Result: "
			pprint(result)

		return result

	def getTopKeywords(self, keywords, wordCount, source, category):
		# Add getting top keywords in the database here
		for keyword in keywords:
			articleScore = 1.0 * keyword['count'] / wordCount
			keyword['totalScore'] = articleScore * 1.5

		return keywords

	def sortScore(self, dictList):
		return sorted(dictList, key=lambda x: -x['totalScore'])

	def sortSentences(self, dictList):
		return sorted(dictList, key=lambda x: x['order'])

	def computeScore(self, sentences, titleWords, topKeywords):
		"""
		Inti algoritma TextTeaser, menghitung skor masing-masing fitur yang akan diambil.
		seperti:
		1. Skor elemen judul.
		2. Skor panjang kalimat.
		3. Skor posisi kalimat.
		4. Skor frekuensi keyword berdasarkan nilai summation-based selection (SBS)
		   dan density-based selection (DBS).

		Kemudian keempat elemen dihitung lagi menggunakan persamaan (8) pp. 12 (Jan, 10)

		:param sentences: List kalimat dalam teks berita.
		:param titleWords: List kata dalam judul.
		:param topKeywords: Dictionary top keyword yang diperoleh.
		:return: Dictionary skor masing-masing kalimat.
		"""

		# Mengambil 10 top keyword dari key "word" yang berguna
		# untuk mendapatkan kata-kata dalam var dict.
		keywordList = [keyword['word'] for keyword in topKeywords]

		# Banyak kalimat dalam teks berita
		sentences_length = len(sentences)

		# List untuk manampung hasil ringkasan.
		summaries = []

		# Enumerate berfungsi supaya loop bisa bersamaan dengan index ('i')
		# blok yang akan diulang adalah : i dan sentence
		for i, sentence in enumerate(sentences):
			if is_log: print ("\n\n-------------------------------")
			if is_log: print ("\nCOMPUTE Sentence: %d:%s\n" % (i, sentence.strip()))

			# Menghapus tanda baca pada kalimat-kalimat dalam teks
			sent = self.parser.removePunctations(sentence)

			# Memotong setiap kata dalam kalimat
			words = self.parser.splitWords(sent)

			# Density-based selection
			if is_log: print ("\nGet 1. DBS feature started.\nDBS Feature for: %s\nKeyword: %s" % (words, keywordList))
			dbsFeature = self.dbs(words, topKeywords, keywordList)
			if is_log: print ("Score: %f" % (dbsFeature))

			# Mendapatkan fitur SBS dan DBS
			# Summation-based selection
			if is_log: print ("\nGet 2. SBS feature started.\nSBS Feature for: %s\n" % words)
			sbsFeature = self.sbs(words, topKeywords, keywordList)
			if is_log: print ("Score: %f" % (sbsFeature))

			# Fitur kemiripan kalimat dengan judul
			if is_log: print ("\nGet 3. title feature started")
			titleFeature = self.parser.getTitleScore(titleWords, words)
			# !!! Printed on target function

			# Skor panjang kalimat dari Ideal = 20.0
			if is_log: print ("\nGet 4. Sentence Length feature started")
			sentenceLength = self.parser.getSentenceLengthScore(words)
			# !!! Printed on target function

			# Skor posisi kalimat dalam teks
			# Params: 
			# i = Posisi kalimat dalam teks, 
			# sentences_length = Jumlah semua kalimat yg ada
			if is_log: print ("\nGet 5. Sentence Position feature started")
			sentencePosition = self.parser.getSentencePositionScore(i, sentences_length)
			# !!! Printed on target function

			# Frekuensi keyword
			if is_log: print ("\nGet 6. keywordFrequency feature started")
			keywordFrequency = (sbsFeature + dbsFeature) / 2.0 * 10.0
			if is_log: print "keywordFrequency = (%f + %f) / 2.0 * 10.0 = %f" % (
			sbsFeature, dbsFeature, keywordFrequency)

			totalScore = (
			             titleFeature * 1.5 + keywordFrequency * 2.0 + sentenceLength * 0.5 + sentencePosition * 1.0) / 4.0

			if is_log: print "Total score %d: (%f * 1.5 + %f * 2.0 + %f * 0.5 + %f * 1.0) / 4.0 = %f" % \
			                 (i, titleFeature, keywordFrequency, sentenceLength, sentencePosition, totalScore)

			summaries.append({
				'totalScore': totalScore,
				'sentence': sentence,
				'order': i
			})

		return summaries

		# Params:
		# words: Kata-kata dalam kalimat

	def sbs(self, words, topKeywords, keywordList):
		score = 0.0

		# if is_log: print "SBS\nWords: %s" 

		if len(words) == 0:
			return 0

		for word in words:
			word = word.lower()
			index = -1
			# Indentation ditambah (9 Des)
			if word in keywordList:
				index = keywordList.index(word)

			if index > -1:
				score += topKeywords[index]['totalScore']

		if is_log: print("Total score: %f" % (score))
		return 1.0 / abs(len(words)) * score

		# Density-based selection
		# Params:
		# words: Kata-kata dalam kalimat

	def dbs(self, words, topKeywords, keywordList):

		# Menghitung kata dalam kalimat yang ada juga dalam top keyword tambah 1
		k = len(list(set(words) & set(keywordList))) + 1
		summ = 0.0
		firstWord = {}
		secondWord = {}

		for i, word in enumerate(words):
			if word in keywordList:
				if is_log: print "\"%s\" FOUND in keyword. i: %d" % (word, i)
				# Indeks kata pada top keyword
				index = keywordList.index(word)

				if firstWord == {}:
					firstWord = {'i': i, 'score': topKeywords[index]['totalScore']}
					if is_log: print("0. firstWord i: %f, score: %f" % (firstWord['i'], firstWord['score']))
				else:
					secondWord = firstWord
					firstWord = {'i': i, 'score': topKeywords[index]['totalScore']}
					distance = firstWord['i'] - secondWord['i']

					if is_log: print("1. firstWord i: %d, score: %f" % (firstWord['i'], firstWord['score']))
					if is_log: print("2. secondWord i: %d, score: %f" % (secondWord['i'], secondWord['score']))
					if is_log: print("3. Distance, %d-%d: %d" % (firstWord['i'], secondWord['i'], distance))
					if is_log: print("4. Summ: %f" % ((firstWord['score'] * secondWord['score']) / (distance ** 2)))

					summ += (firstWord['score'] * secondWord['score']) / (distance ** 2)

				# print "\"%s\" NOT in keyword. i: %d" % (word, i)

		if is_log: print("(1.0 / %d * (%d + 1.0)) * %f" % (k, k, summ))

		return (1.0 / k * (k + 1.0)) * summ
