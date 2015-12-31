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
from time import sleep

# Peber Web Model
from peber_web.function.paginating_news import get_paged_news_text
from peber_web.models import News_Source, News
from peber_web.models import UserDesc


# Method to save to database
from .function.database_access import DatabaseAccess

# Pushbots untuk push notif di Android
from pushbots import Pushbots

# Module for news extraction
import feedparser
import newspaper

from urlparse import urlparse

# Generate summary to all news in db
from peber_web.algorithms.peber_summarizer import PeberSummarizer
import re

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


def fetch_news_url(ns_id, ns_source_url):
	"""
	Fungsi untuk mengambil URL dalam halaman Kompas.com atau Liputan6.com
	Kemudian URL akan diperiksa apakah sudah ada dalam database.
	:param ns_id: ID Sumber Berita
	:param ns_source_url: URL Sumber Berita
	:return:
	"""
	# TODO Perhatikan memoize
	print("Fetch news URL started. URL: %s" % ns_source_url)
	news_paper = newspaper.build(ns_source_url, language='id', memoize_articles=False)
	for article in news_paper.articles:
		o = urlparse(ns_source_url)
		news_url = article.url

		# Memastikan url berkaitan dengan ns_source_url
		if news_url.find(o.netloc) != -1:
			is_data_available = News.objects.filter(news_url=news_url).exists()

			if not is_data_available:
				# News Content berisi:
				# - news_title
				# - news_content
				# - news_image_hero
				news_content = get_paged_news_text(news_url)
				news_content['news_corp'] = ns_id
				news_content['news_url'] = news_url
				last_news_id = dbs_task.insert_news_to_db(news_content)

				if last_news_id == 0:
					print("Berita GAGA disimpan! :D")
			else:
				print("Data already available.")


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

	print("%s - Mulai Parsing %s-%s" % (tag, ns_source_publisher, ns_source_category))

	# Jika NS Publisher adalah Kompas atau Liputan 6
	# Karena kedua sumber tersebut tidak ada RSS Feed.
	if ns_source_publisher == "Kompas.com" or ns_source_publisher == "Liputan6.com":
		fetch_news_url(ns_id, ns_source_url)

	# Panggil fungsi parsing RSS feed url. (2 Des)
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
	"""
	print("Execute Parser by Category: %s" % ns_category)

	# Jika kategori 'ALL' maka parse semua berita 
	if ns_category == 'ALL':
		ns_data_category = News_Source.objects.all()
	else:
		ns_data_category = News_Source.objects.filter(source_category=ns_category)

	print("Total NS to Parse: %s" % ns_data_category.count())
	# Masukkan semua worker dalam sebuah list.
	jobs = []
	for news_source in ns_data_category:
		jobs.append(parse_certain_ns_task.s(
			news_source.id,
			news_source.source_publisher,
			news_source.source_category,
			news_source.source_url
		))

	# Grup worker yang akan dieksekusi
	job_group = group(jobs)

	# Jalankan semua worker dalam worker group.
	job_result = job_group.apply_async()

	# return akan otomatis gagal / False
	if job_result.successful():
		return job_result.successful()
	else:
		return False


@shared_task()
def execute_news_parser():
	"""
	Menjalankan parse_news_feed_task. Dengan params data News Source.
	"""
	jobs = []
	for news_source in global_ns_data:
		jobs.append(parse_certain_ns_task.s(
			news_source.id,
			news_source.source_publisher,
			news_source.source_category,
			news_source.source_url
		))

	job_group = group(jobs)

	job_result = job_group.apply_async()
	job_result.get()

	if job_result.successful():
		return job_result.successful()
	else:
		return False


@shared_task()
def parse_all_news_feed_task():
	"""
	Parse all news feed. Bagian untuk mengambil semua data dari RSS Feed.
	"""
	global feed_data  # Var utk insert_database

	for news_source in global_ns_data:  # ns_data News Source Data (Semuanya)

		ns_source_publisher = news_source.source_publisher
		ns_source_category = news_source.source_category
		rss_url = news_source.source_url
		id_corp = news_source.id

		print("Parsing %s-%s" % (ns_source_publisher, ns_source_category))

		try:

			feed_data = feedparser.parse(rss_url)

			data_entri_length = len(feed_data.entries)

			# Jika terdapat data yg dari feedparser
			if not data_entri_length == 0:
				print("Total: %d from %s-%s" % (
					data_entri_length,
					ns_source_publisher,
					ns_source_category))

				# Proses database
				feed_data.news_corp_id = id_corp
				saved_count = dbs_task.insert_news_data(feed_data)

				if not saved_count == 0:
					print("Data berita id: %d berhasil ditambah" % saved_count)
				else:
					logger.warning("Tidak ada berita yang ditambah.")
			# Jika tidak data yg didapat dari feedparser
			else:
				logger.warning("Tidak ada data entri %s-%s" % (
					ns_source_publisher,
					ns_source_category))

		except Exception as ex:
			logger.error("[ERROR] Parsing URL(%d): %s Gagal" % (id_corp, rss_url))
			logger.error("Error Messages: %s" % ex)


@shared_task
def generate_news_summary():
	all_news = News.objects.filter(news_corp__id=8)  # Berita tempo nasional

	for n in all_news:
		news_text = n.news_content.strip()
		news_title = n.news_title

		pbs = PeberSummarizer(re.sub(r'[^\x00-\x7f]', r'', news_text))

		if n.news_summary == 'N/A':
			# n.news_summary = pbs.pebahasa_summarizer()
			n.news_summary = pbs.text_teaser_summarizer(news_title)
			n.save()
		else:
			logger.info('News already summarized.')


# Pushbots untuk push notif di Android
def push_new_news_by_category(user_id):
	""" Push notif untuk Android. (1 Des, 2015)
		Berita yang diberikan pada user adalah 
		berita index berita pertama pada daftar 
		berdasarkan Category.
	"""

	current_user_desc = UserDesc.objects.get(pk=user_id)

	# Data yang akan dikirim ke perangkat.
	push_platform = Pushbots.PLATFORM_ANDROID
	push_msg = "Test Notif - Dimas Ekky dan Andi Gilang Perbaiki Catatan..."
	push_news_id = "3482"
	push_next_activity = "com.unware.peber_android.NewsDetails"

	# Define app_id and secret
	my_app_id = '562f91ef1779594f6f8b4568'
	my_secret = '3a0ac7d0c28c665396d0bc441382ed30'
	# Create a Pushbots instance
	pushbots = Pushbots(app_id=my_app_id, secret=my_secret)

	# Define data
	data = {'platform': push_platform, 'msg': push_msg,
	        'payload': {'news_id': push_news_id, 'nextActivity': push_next_activity}}

	# Alternatively you can set 'except_alias' : 'superjohn123' to exclude
	# "superjohn123" from getting that push
	code, msg = pushbots.push_batch(data=data)
	print('Returned code: {0}'.format(code))
	print('Returned message: {0}'.format(msg))


# Learn how to send task progress status
@celery_app.task()
def add(x, y):
	add.update_state(state='PROGRESS', meta={'progress': 0})
	sleep(30)
	add.update_state(state='PROGRESS', meta={'progress': 30})
	sleep(30)
	return x + y


def get_task_status(task_id):
	# If you have a task_id, this is how you query that task
	task = add.AsyncResult(task_id)

	status = task.status
	progress = 0

	if status == u'SUCCESS':
		progress = 100
	elif status == u'FAILURE':
		progress = 0
	elif status == 'PROGRESS':
		progress = task.info['progress']

	return {'status': status, 'progress': progress}


@celery_app.task()
def periodic_helo():
	print("Hello Celery World Tasks!")
