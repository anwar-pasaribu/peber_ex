# coding=utf-8
from __future__ import division, print_function, unicode_literals

from sumy.parsers.plaintext import PlaintextParser
from sumy.evaluation.coselection import f_score
from sumy.evaluation.coselection import precision
from sumy.evaluation.coselection import recall
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

# Peber model
from peber_web.models import News

import peber_web.function.timing

LANGUAGE = "english"
SENTENCES_COUNT = 5
# Take news filter by Tempo-Berita Terbaru
news_tempo = News.objects.all()


def run_sumy_eval_test():
	for news in news_tempo:
		news_content = news.news_content
		text_teaser_summary = news.news_summary

		parser = PlaintextParser.from_string(news_content, Tokenizer(LANGUAGE))
		stemmer = Stemmer(LANGUAGE)

		summarizer = Summarizer(stemmer)
		summarizer.stop_words = get_stop_words('indonesia')
		text_rank_summary_res = ""
		for sentence in summarizer(parser.document, SENTENCES_COUNT):
			text_rank_summary_res = "%s%s\n\n" % (text_rank_summary_res, sentence)
			# print(sentence)

		news.news_text_rank_summary = text_rank_summary_res

		reference_summary = text_rank_summary_res
		evaluated_summ = text_teaser_summary

		# Menghitung score
		reference_document = PlaintextParser.from_string(reference_summary, Tokenizer(LANGUAGE))
		reference_sentences = reference_document.document.sentences

		evaluated_doc = PlaintextParser.from_string(evaluated_summ, Tokenizer(LANGUAGE))
		evaluated_sent = evaluated_doc.document.sentences

		f_score_res = f_score(evaluated_sent, reference_sentences)
		p_res = precision(evaluated_sent, reference_sentences)
		re_res = recall(evaluated_sent, reference_sentences)

		news.f_score = f_score_res
		news.precision = p_res
		news.recall = re_res

		news.save()
