import logging
from gensim import corpora, models, similarities
from collections import defaultdict
from pprint import pprint   # pretty-printer

stoplist = set('for a of the and to in'.split())  # Hasil berupa dictionary
dictionary = corpora.Dictionary(line.lower().split() for line in open('mycorpus.txt'))

class MyCorpus(object):
     def __iter__(self):
         for line in open('mycorpus.txt'):
             # assume there's one document per line, tokens separated by whitespace
             yield dictionary.doc2bow(line.lower().split())
			 
if __name__ == '__main__':
	corpus_memory_friendly = MyCorpus() # doesn't load the corpus into memory!
	print(corpus_memory_friendly)
	
	for vector in corpus_memory_friendly: # load one vector into memory at a time
		print(vector)