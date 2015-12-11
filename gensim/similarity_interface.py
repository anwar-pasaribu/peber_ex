import logging
from gensim import corpora, models, similarities
from collections import defaultdict
from pprint import pprint   # pretty-printer

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

dictionary = corpora.Dictionary.load('deerwester.dict')
corpus = corpora.MmCorpus('deerwester.mm') # comes from the first tutorial, "From strings to vectors"
print("Data corpus:")
print(corpus)

# To follow Deerwester's example, we first use this tiny corpus to define a 2-dimensional LSI space:
lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=2)

# Latihan mencari sesuatu
doc = "Human machine interface for lab abc computer"
vec_bow = dictionary.doc2bow(doc.lower().split())
vec_lsi = lsi[vec_bow] # convert the query to LSI space
print(vec_lsi)

# Mempersiapkan similarity query
index = similarities.MatrixSimilarity(lsi[corpus]) # transform corpus to LSI space and index it
index.save('deerwester.index')

# Index sekarang diambil dari static files
index = similarities.MatrixSimilarity.load('deerwester.index')

# Performing query
sims = index[vec_lsi] # perform a similarity query against the corpus

# print (document_number, document_similarity) 2-tuples
print("\nPerforming query")
print(list(enumerate(sims)))

# With some standard Python magic we sort these similarities into descending order
sims = sorted(enumerate(sims), key=lambda item: -item[1])

# Cetak similarities yang sudah diringkas
print("\nCetak similarities yang sudah disortir")
pprint(sims)











