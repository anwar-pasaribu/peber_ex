import logging
from gensim import corpora, models, similarities
from collections import defaultdict
from pprint import pprint   # pretty-printer

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

documents = [line.rstrip('\n') for line in open('mycorpus.txt')]

# Menghilangkan stopword
stoplist = set('for a of the and to in'.split())  # Hasil berupa dictionary
texts = [ [word for word in document.lower().split() if word not in stoplist] for document in documents]

# Menghilangkan kata yg hanya muncul sekali
frequency = defaultdict(int)
for text in texts:
    for token in text:
        frequency[token] += 1

texts = [ [token for token in text if frequency[token] > 1] for text in texts]

# Hasil teks yg sudah bersih

# Menyimpan dictinary ke hardisk
dictionary = corpora.Dictionary(texts)
dictionary.save('deerwester.dict')  # Menyimpan dict ke hdd


# Menyimpan mmCorpus ke hdd
corpus = [ dictionary.doc2bow(text) for text in texts ]
corpora.MmCorpus.serialize('deerwester.mm', corpus)  # Menimpan corpus utk penggunaan later

class MyCorpus(object):
     def __iter__(self):
         for line in open('mycorpus.txt'):
             # assume there's one document per line, tokens separated by whitespace
             yield dictionary.doc2bow(line.lower().split())
			 
			 
corpus_memory_friendly = MyCorpus() # doesn't load the corpus into memory!
print(corpus_memory_friendly)

for vector in corpus_memory_friendly: # load one vector into memory at a time
	print(vector)