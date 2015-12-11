__author__ = 'Anwar Pasaribu'

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

str = "Saya sangat dengan kuliah bersama Prof. Opim tadi pagi. Pengatar: OOP sangat mudah dipahami. Suka sekali dengan Prof. Opim."
stop_word = set(stopwords.words("indonesia"))

# Menghapus stopword dalam array of string
filtered_word = [w for w in word_tokenize(str) if w not in stop_word ]

print filtered_word