import feedparser

from peber_web.tasks import get_single_feed_task

# Contoh sumber RSS
url_sources = [
	"http://sindikasi.okezone.com/index.php/techno/RSS2.0",  # Okezone Tekno
	"http://detik.feedsportal.com/c/33613/f/656095/index.rss",  # Detik Tekno
	"http://www.antara.co.id/rss/tek.xml",  # ANTARA News Teknologi
	"http://rss.tempo.co/index.php/teco/news/feed/start/0/limit/10/kanal/10"  # Tempo.co Tekno
]


class RssFeedParser:
	"""
	Untuk mengambil link berita dari RSS Feed
	"""
	url_sources

	def add_source(self, url_source):
		self.url_sources.append(url_source)

	def get_feeds(self):
		feeds = []
		for url_source in url_sources:
			feeds.append(feedparser.parse(url_source))
		return feeds

	def get_single_feed(self, url):
		data = get_single_feed_task.delay(url.source_url)
		data.news_corp_id = url.id
		return data

	# Untuk mencetak data ke konsol
	def print_news(self, data):
		i = 0
		for post in data.entries:		
			print("{0} : {1}".format(i+1, post.title, post.title))
			i = i + 1
		i = 0



