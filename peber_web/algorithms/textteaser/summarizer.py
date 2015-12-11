#!/usr/bin/python
# -*- coding: utf-8 -*-
from .parser import Parser

# menentukan log ditampilkan atau tidak
is_log = True

class Summarizer:

	def __init__(self):
		self.parser = Parser()

	def summarize(self, text, title, source, category):

		# Preprocessing
		sentences = self.parser.splitSentences(text)  # Memotong menjadi kalimat
		titleWords = self.parser.removePunctations(title)  # Menghapus tanda baca
		titleWords = self.parser.splitWords(title)  # Memisahkan menjadi kata

		# Bagian untuk hapus stopword
		(keywords, wordCount) = self.parser.getKeywords(text)

		# Mengambil 10 top keyword
		topKeywords = self.getTopKeywords(keywords[:10], wordCount, source, category)
		if is_log: print "Topkeywords: %s\n" % topKeywords

		result = self.computeScore(sentences, titleWords, topKeywords)
		if is_log: print "Compute Score Result: %s" % result

		result = self.sortScore(result)
		if is_log: print "Sort Score Result: %s" % result

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

	# Inti algoritma, menghitung skor masing-masing fitur yang akan diambil.
	def computeScore(self, sentences, titleWords, topKeywords):

		# Mengambil 10 top keyword dari key "word" yang berguna
		# untuk mendapatkan kata-kata dalam var dict.
		keywordList = [keyword['word'] for keyword in topKeywords]

		# List untuk manampung hasil ringkasan.
		summaries = []

		# Enumerate berfungsi supaya loop bisa bersamaan dengan index ('i')
		# blok yang akan diulang adalah : i dan sentence
		for i, sentence in enumerate(sentences):
			# Menghapus tanda baca pada kalimat-kalimat dalam teks
			sent = self.parser.removePunctations(sentence)

			# Memotong setiap kata dalam kalimat
			words = self.parser.splitWords(sent)

			# Mendapatkan fitur SBS dan DBS
			# Summation-based selection
			sbsFeature = self.sbs(words, topKeywords, keywordList)

			# Density-based selection
			dbsFeature = self.dbs(words, topKeywords, keywordList)

			# Fitur kemiripan kalimat dengan judul
			titleFeature = self.parser.getTitleScore(titleWords, words)

			# Skor panjang kalimat dari Ideal = 20.0
			sentenceLength = self.parser.getSentenceLengthScore(words)

			# Skor posisi kalimat dalam teks
			sentencePosition = self.parser.getSentencePositionScore(i, len(sentences))

			# Frekuensi keyword
			keywordFrequency = (sbsFeature + dbsFeature) / 2.0 * 10.0
			if is_log: print "keywordFrequency = (%f + %f) / 2.0 * 10.0 = %f" % (sbsFeature, dbsFeature, keywordFrequency)

			totalScore = (titleFeature * 1.5 + keywordFrequency * 2.0 + sentenceLength * 0.5 + sentencePosition * 1.0) / 4.0

			if is_log: print "Total score %d: (%f * 1.5 + %f * 2.0 + %f * 0.5 + %f * 1.0) / 4.0 = %f\n\n" % \
				(i, titleFeature, keywordFrequency, sentenceLength, sentencePosition, totalScore)

			summaries.append({
				# 'titleFeature': titleFeature,
				# 'sentenceLength': sentenceLength,
				# 'sentencePosition': sentencePosition,
				# 'keywordFrequency': keywordFrequency,
				'totalScore': totalScore,
				'sentence': sentence,
				'order': i
			})

		return summaries

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

		return 1.0 / abs(len(words)) * score

	# Density-based selection
	def dbs(self, words, topKeywords, keywordList):
		k = len(list(set(words) & set(keywordList))) + 1
		summ = 0.0
		firstWord = {}
		secondWord = {}

		for i, word in enumerate(words):
			if word in keywordList:
				index = keywordList.index(word)

				if firstWord == {}:
					firstWord = {'i': i, 'score': topKeywords[index]['totalScore']}
				else:
					secondWord = firstWord
					firstWord = {'i': i, 'score': topKeywords[index]['totalScore']}
					distance = firstWord['i'] - secondWord['i']

					summ += (firstWord['score'] * secondWord['score']) / (distance ** 2)

		return (1.0 / k * (k + 1.0)) * summ
