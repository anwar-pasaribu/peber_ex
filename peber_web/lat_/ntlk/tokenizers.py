from nltk.tokenize import TreebankWordTokenizer
from nltk.tokenize import sent_tokenize, word_tokenize

class Tokenizer(object):
	def word_tkn(self, str):
		tkn = TreebankWordTokenizer()
		return tkn.tokenize(str)

if __name__ == '__main__':
	tok = Tokenizer()
	str = "Saya sangat dengan kuliah bersama Prof. Opim tadi. Pengatar: OOP sangat mudah dipahami. Suka banget! dengan Prof. Opim."

	print tok.word_tkn(str)

	print sent_tokenize(str)
	print word_tokenize(str)