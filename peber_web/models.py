# coding=utf-8
from time import time

from django.db import models
from django.contrib.auth.models import User

from peber_web.function.news_extractors import format_news_content_texts


# Method utk upload
# noinspection PyUnusedLocal
def get_upload_file_name(instance, filename):
	clear_filename = str(filename.replace(' ', '_'))
	return "peber_web/images/user_pp/%s_%s" % (str(time()).replace('.', '_'), clear_filename)


# Create your models here.

# noinspection PyPep8Naming
class News_Source(models.Model):
	source_publisher = models.CharField(max_length=100)
	source_category = models.CharField(max_length=100)
	source_url = models.TextField()

	def __str__(self):  # diperlukan utk debugging
		return "{0}-{1}".format(
			self.source_publisher,
			self.source_category)

	def __unicode__(self):  # Dari Mike Hibbert Pyhon 2
		return "{0}-{1}".format(
			self.source_publisher,
			self.source_category)


class News(models.Model):
	news_url = models.TextField()
	news_title = models.TextField()
	news_content = models.TextField()
	news_corp = models.ForeignKey(News_Source, related_name='news_sources')  # ID sumber (Foreign key dari News_Source)

	news_summary_lex_rank = models.TextField(blank=True)  # A1 Summarization
	news_summary_lsa = models.TextField(blank=True)  # A2 Summarization
	news_summary_text_rank = models.TextField(blank=True)  # A3 Summarization

	# Lex Rank
	a1_f_score = models.DecimalField(max_digits=7, decimal_places=6, default=0)
	a1_precision = models.DecimalField(max_digits=7, decimal_places=6, default=0)
	a1_recall = models.DecimalField(max_digits=7, decimal_places=6, default=0)

	# LSA Algorithm evaluation
	a2_f_score = models.DecimalField(max_digits=7, decimal_places=6, default=0)
	a2_precision = models.DecimalField(max_digits=7, decimal_places=6, default=0)
	a2_recall = models.DecimalField(max_digits=7, decimal_places=6, default=0)

	news_pub_date = models.DateTimeField()
	news_image_hero = models.TextField()

	class Meta(object):
		ordering = ['-news_pub_date', ]

	def news_content_web_format(self):
		# my_texts = self.news_content.replace('\n', '<br /><br />')
		my_texts = format_news_content_texts(self.news_corp.id, self.news_content, '<br /><br />')

		return "<em>Formatted</em>:<br />{0}<p align='center'>***</p>".format(my_texts)

	def __str__(self):
		return "{0} ({1})".format(self.news_title, self.news_corp)

	def __unicode__(self):
		return u'{c} ({l})'.format(c=self.news_title, l=self.news_corp)


class UserDesc(models.Model):
	user = models.ForeignKey(User, related_name='userdescs')  # DRF Suggest
	news_choices = models.ManyToManyField(News_Source, blank=True)
	bio = models.TextField(blank=True)
	# Upload file by Mike Hibbert
	profile_pict = models.ImageField(upload_to=get_upload_file_name, blank=True)

	# Berita yang sudah dibaca (1 Des, 2015)
	read_news = models.ManyToManyField(News, blank=True)

	def __unicode__(self):
		return self.user.get_username()

	def __str__(self):  # __unicode__ on Python 2
		return "{0}: {1} News Sources".format(self.user.get_username(), len(self.news_choices.all()))
