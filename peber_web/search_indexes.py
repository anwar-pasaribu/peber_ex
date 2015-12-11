import datetime
from haystack import indexes
from peber_web.models import News


class NewsIndex(indexes.SearchIndex, indexes.Indexable):
	text = indexes.CharField(document=True, use_template=True)  # Main info yg akan diindeks
	pub_date = indexes.DateField(model_attr='news_pub_date')

	# Teks yg ditampilkan pada autocomplete
	content_auto = indexes.EdgeNgramField(model_attr='news_title')

	def get_model(self):
		return News

	def index_queryset(self, using=None):
		"""
		Used when the entire index for model is updated.
		"""
		return self.get_model().objects.all()
		# return self.get_model().objects.filter(news_pub_date__lte=datetime.datetime.now())
