# Kelas untuk memuat data korpus
# 5 Sep 2015

import nltk.data
import yaml
from nltk.corpus.reader import WordListCorpusReader

cust_corpora_path_root = "corpora/cookbook/mywords.txt"

class CustomCorpora():
	def __init__(self, path=cust_corpora_path_root):
		self.path = nltk.data.find(path)

	def raw_loader(self):
		return nltk.data.load(self.path, format='raw')

	def yaml_loader(self):
		return nltk.data.load(self.path)

	def word_list_loader(self):
		return WordListCorpusReader(self.path, ['wordlist'])