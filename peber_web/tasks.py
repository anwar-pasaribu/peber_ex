# coding=utf-8
from __future__ import absolute_import
from celery import shared_task
from celery import group
from celery.utils.log import get_task_logger

# Test Ensuring a task is only executed one at a time
from django.core.cache import cache
from hashlib import md5

# Celery instance in parent project (peber_ex)
# Oct 22
from peber_ex import celery_app

# Peber Web Model
from peber_web.function.paginating_news import get_paged_news_text
from peber_web.models import News_Source, News

# Method to save to database
from .function.database_access import DatabaseAccess

# Pushbots untuk push notif di Android
from pushbots import Pushbots

# Module for news extraction
import feedparser
import newspaper
from goose import Goose

from urlparse import urlparse

# Masalah ketika parsing kompas, newspaper tidak lengkap
from bs4 import BeautifulSoup

# Latihan Lock_Expire untuk helo_task(nama) 
# 1 Des 2015

LOCK_EXPIRE = 60 * 5  # Lock expires in 5 minutes

# Menampilkan log pada terminal worker
logger = get_task_logger(__name__)

# Instance akses database
dbs_task = DatabaseAccess()
global_ns_data = dbs_task.get_all_news_source()

# Control logger, whether show or no
LOG = True


# Task with schedule
@celery_app.task()
def helo_task(nama):
	feed_url_hexdigest = md5(nama).hexdigest()
	lock_id = '{0}-lock-{1}'.format("coba", feed_url_hexdigest)

	# Mendapatkan ID task yg dijalankan
	print("ID Hello: %s" % helo_task.request.id)

	# Lambda function untuk membatasi akses database sekaligus secara bersamaan (2 Des)
	acquire_lock = lambda: cache.add(lock_id, 'true', LOCK_EXPIRE)
	release_lock = lambda: cache.delete(lock_id)

	logger.debug('Importing feed: %s', nama)

	if acquire_lock():
		try:
			nama = "%s" % nama
		finally:
			release_lock()
		# sleep(10)
		return "Hello {n}!".format(n=nama)

	# sleep(5)  # Ecek-ecek sleep utk 5 detik
	# return "Hello {n} Bitches!".format(n=nama)
	logger.debug('Feed %s is already being imported by another worker', nama)


# Fungsi untuk insert database.
def call_insert_news_data(data):
	"""
	Menyimpan data jika data belum ada di database.
	:return Jumlah data yang berhasil dimasukkan.
	"""
	tag = "Insert News Data"

	id_news_source = 'ns_id{0}'.format(data.news_corp_id)

	feed_url_hexdigest = md5(id_news_source).hexdigest()
	lock_id = '{0}-lock-{1}'.format(id_news_source, feed_url_hexdigest)

	# Lambda function untuk membatasi akses database sekaligus secara bersamaan (2 Des)
	acquire_lock = lambda: cache.add(lock_id, 'true', LOCK_EXPIRE)
	release_lock = lambda: cache.delete(lock_id)

	print('%s - Mulai menyimpan feed, id: %s' % (tag, id_news_source))
	count_data_added = 0  # Jumlah data yang berhasil ditambah

	if acquire_lock():
		try:
			count_data_added = dbs_task.insert_news_data(data)
			if count_data_added is not 0:
				print("%s - Successfully save %d items." % (tag, count_data_added))
			else:
				print("%s - Fail, No data saved." % tag)

		finally:
			print("%s - Finally Saving data finished. Save %d items." % (tag, count_data_added))
			release_lock()
		# sleep(10)
		return count_data_added

	# Worker lain melakukan penyimpanan
	print('%s - Data id: %s is already being saved by another worker' % (tag, id_news_source))
	return count_data_added


# Function untuk parse rss
def rss_feed_parser(rss_url):
	"""
	Fungsi untuk parsing feed url.
	:return Data hasil parsing RSS atau 0 jika tidak ada data.
	"""
	tag = "Feed Parser"  # Tag untuk keperluan logging

	feed_datas = feedparser.parse(rss_url)

	# Bozo == 1 berarti gagal mengambil data RSS.
	if feed_datas.bozo is not 1:
		print("Hasil parsing akan diolah dari url: %s" % rss_url)
		return feed_datas
	else:
		print("%s - Tidak ada hasil parsing dari URL: %s" % (tag, rss_url))
		return 0


def fetch_news_url(ns_id, ns_category, ns_source_url):
	"""
	Fungsi untuk mengambil URL dalam halaman Kompas.com atau Liputan6.com
	Kemudian URL akan diperiksa apakah sudah ada dalam database.
	:param ns_id: ID Sumber Berita
	:param ns_source_url: URL Sumber Berita
	:param ns_category: Kategori berita, berguna untuk mengirim push notif
	"""
	o = urlparse(ns_source_url)
	urls = []

	print("Fetching news URL. URL: %s" % o.netloc)

	if ns_source_url.find('kompas.com') != -1:
		# Inisialisasi Python Goose
		goose_instance = Goose()
		article = goose_instance.extract(url=ns_source_url)
		main_soup = BeautifulSoup(article.raw_html)
		for tag in main_soup.find_all('a'):
			if tag.get('href').find("%s/read" % o.netloc) != -1:
				urls.append(tag.get('href').rsplit('?')[0])  # Menghapus url params dari url

	elif ns_source_url.find('liputan6.com') != -1:
		# Memoize artikel ditujukan untuk menghindari mengingat data yang di olah sebelumnya.
		news_paper = newspaper.build(ns_source_url, language='id', memoize_articles=False)
		for article in news_paper.articles:
			news_url = article.url
			# Memastikan url berkaitan dengan ns_source_url
			if news_url.find(o.netloc) != -1:
				urls.append(news_url)

	# Untuk memesatikan tidak ada URL yang sama.
	url_set = list(set(urls))

	print("Found %d news URL." % len(url_set))

	# Periksa apakah ada URL hasil ekstraksi halaman web.
	if len(url_set) == 0:
		return None

	# Total berita yang berhasil dimasukkan dalam database
	added_news_id = []
	for news_url in url_set:
		# Periksa keberadaan data dalam database berdasarkan URL berita.
		is_data_available = News.objects.filter(news_url=news_url).exists()
		if not is_data_available:
			# News Content berisi:
			# - news_title
			# - news_content
			# - news_image_hero (URL)
			news_content = get_paged_news_text(news_url)
			if news_content is not None:
				news_content['news_corp'] = ns_id
				news_content['news_url'] = news_url
				last_news_id = dbs_task.insert_news_to_db(news_content)

				# Periksa apakah berita berhasil disimpan.
				if last_news_id != 0:
					# Total jumlah berita ditambahkan 1 jika berhasil insert ke database.
					added_news_id.append(last_news_id)
				else:
					print("Berita gagal disimpan!.\nURL: %s" % news_url)
			else:
				print("News Contents kosong atau tidak valid pada URL:\nURL: %s" % news_url)
		else:
			print("Data sudah ada dalam database.")

	# TODO Need more attentions!!!
	# Mengirim notifikasi berdasarkan kategori berita
	# pada aplikasi klien (Android Apps)
	# menggunakan sistem PushBots (Jan, 10th)
	len_added_news_id = len(added_news_id)
	if len_added_news_id != 0:
		# Dari total berita yang diambil akan push satu berita
		news_id = added_news_id[len_added_news_id - 1]

		if news_id != 0:
			# ns_category: Sebagai tag kemana berita akan di push.
			push_new_news_by_category(news_id, ns_category)


@shared_task()
def parse_certain_ns_task(ns_id, ns_publisher, ns_category, ns_url):
	"""
	Bagian untuk mengambil data dari RSS Feed yg diberikan.
	@params: news_source: Data sumber berita.
	"""
	tag = "Parse Certain NS"

	# Data NS yang akan diparsing
	ns_id = ns_id
	ns_source_publisher = ns_publisher
	ns_source_category = ns_category
	ns_source_url = ns_url

	print("%s - Mulai RSS Parsing %s-%s" % (tag, ns_source_publisher, ns_source_category))

	# Jika NS Publisher adalah Kompas atau Liputan 6
	# Karena kedua sumber tersebut tidak ada RSS Feed maka URL berita diambil dengan cara
	# menelusuri tag a dalam dokumen HTML.
	if ns_source_publisher == "Kompas.com" or ns_source_publisher == "Liputan6.com":
		fetch_news_url(ns_id, ns_category, ns_source_url)

	# Panggil fungsi parsing RSS feed url. (2 Des)
	# Feedparser ditujukan untuk detik.com karena memeiliki RSS Feed
	parsed_feed = rss_feed_parser(ns_source_url)

	# Jika terdapat data yg dari feedparser
	if parsed_feed is not 0:
		print("%s - Total: %d from %s-%s" % (tag, len(parsed_feed.entries), ns_source_publisher, ns_source_category))

		# Proses database pada fungsi (2 Des)
		parsed_feed.news_corp_id = ns_id  # Selipkan data ID News Source, utk news extractor.
		call_insert_news_data(parsed_feed)

	# Jika tidak data yg didapat dari feedparser
	else:
		print("%s - Tidak ada data entri %s-%s" % (
			tag,
			ns_source_publisher,
			ns_source_category))


@shared_task()
def execute_parser_by_category(ns_category):
	"""
	Menjalankan parse_certain_ns_task. Dengan parameter data NS Category.
	Terdapat tiga tipe parameter:
	1. 'ALL' : Mengacu pada semua News Source
	2. 'pub:NewsPublisher' : Memperoleh data berdasarkan penyedia berita.
	3. 'category' : Berdasarkan kategori spesifik yg diminta
	"""
	print("Execute Parser by Category: %s" % ns_category)

	if ns_category == 'ALL':
		ns_data_category = News_Source.objects.all()
	elif len(ns_category.split(':')) == 2:
		ns_data_category = News_Source.objects.filter(source_publisher=ns_category.split(':')[1])
	else:
		ns_data_category = News_Source.objects.filter(source_category=ns_category)

	print("Total NS to Parse: %s" % ns_data_category.count())
	# Masukkan semua worker dalam sebuah list.

	jobs = []
	for news_source in ns_data_category:
		jobs.append(
			parse_certain_ns_task.s(  # Task yang akan dijalankan
				news_source.id,
				news_source.source_publisher,
				news_source.source_category,
				news_source.source_url
			))

	# Grup worker yang akan dieksekusi
	job_group = group(jobs)

	# Jalankan semua worker dalam worker group.
	job_group.apply_async()


def example_generic_put(tags, message):
	"""Example api call using put request"""

	# Define app_id and secret
	my_app_id = '562f91ef1779594f6f8b4568'
	my_secret = '3a0ac7d0c28c665396d0bc441382ed30'
	# Create a Pushbots instance
	pushbots = Pushbots(app_id=my_app_id, secret=my_secret)
	# Define the API url
	api_url = 'https://api.pushbots.com/push/all'
	# Define your headers manually or use the one's from Pushbots module
	headers = pushbots.headers  # or define yours as a python dict
	# Define your data accordingly, or define no data
	data = {'platform': '1', 'tags': tags, "msg": message}
	# data = {'platform': '1', 'alias': 'anwars', "msg" : "To Anwar,  hi from PyPush."}
	code, msg = pushbots.post(api_url=api_url, headers=headers, data=data)
	print('Returned code: {0}'.format(code))
	print('Returned message: {0}'.format(msg))


def push_new_news_by_category(news_id, tag):
	""" Push notif untuk Android. (1 Des, 2015)
		Berita yang diberikan pada user adalah 
		berita index berita terakhir pada daftar
		berdasarkan Category.
	"""

	current_news = News.objects.get(pk=news_id)
	first_sent_summary = current_news.news_summary.split('\n\n')[0]

	# Data yang akan dikirim ke perangkat.
	push_platform = Pushbots.PLATFORM_ANDROID
	custom_notif_title = "%s..." % current_news.news_title[:50]
	img_url = current_news.news_image_hero
	summary_text = first_sent_summary
	push_news_id = news_id
	push_next_activity = "com.unware.peber_android.NewsDetails"
	tags = [tag]

	# Define app_id and secret
	my_app_id = '562f91ef1779594f6f8b4568'
	my_secret = '3a0ac7d0c28c665396d0bc441382ed30'
	# Create a Pushbots instance
	pushbots = Pushbots(app_id=my_app_id, secret=my_secret)

	# Define data
	data = {'platform': push_platform, 'msg': first_sent_summary,
			'tags': tags,
	        'payload': {'news_id': push_news_id,
	                    'customNotificationTitle': custom_notif_title,
	                    'BigPictureStyle': 'true',
	                    'imgUrl': img_url,
	                    'summaryText': summary_text,
	                    'nextActivity': push_next_activity}}

	# Alternatively you can set 'except_alias' : 'superjohn123' to exclude
	# "superjohn123" from getting that push
	code, msg = pushbots.push_batch(data=data)
	print('Returned code: {0}'.format(code))
	print('Returned message: {0}'.format(msg))
