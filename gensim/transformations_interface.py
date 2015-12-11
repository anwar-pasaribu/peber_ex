import logging
from gensim import corpora, models, similarities
from collections import defaultdict
from pprint import pprint   # pretty-printer

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

dictionary = corpora.Dictionary.load('deerwester.dict')
corpus = corpora.MmCorpus('deerwester.mm')

print(corpus)

# Creating a transformation
tfidf = models.TfidfModel(corpus) # step 1 -- initialize a model

# Transforming vectors
doc_bow = [(0, 1), (1, 1)]
print tfidf[doc_bow]

# Or to apply a transformation to a whole corpus:
corpus_tfidf = tfidf[corpus]
for doc in corpus_tfidf:
	print doc
	
#  Latent Semantic Indexing
lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=2) # initialize an LSI transformation
corpus_lsi = lsi[corpus_tfidf] # create a double wrapper over the original corpus: bow->tfidf->fold-in-lsi
lsi.print_topics(2)

print '\n'
for doc in corpus_lsi: # both bow->tfidf and tfidf->lsi transformations are actually executed here, on the fly
	print doc