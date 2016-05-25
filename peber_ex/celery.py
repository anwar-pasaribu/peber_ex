# coding=utf-8
from __future__ import absolute_import

import os
from celery import Celery
from celery.schedules import crontab

from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'peber_ex.settings')

app = Celery('peber_ex')


# Class to rule the celery
class Config(object):
	# Setting for celery
	def __init__(self):
		pass

	CELERY_TASK_SERIALIZER = 'json'
	CELERY_ACCEPT_CONTENT = ['json', 'pickle']

	# Broker RabbitMQ, broker bawaan celery
	BROKER_URL = 'amqp://guest:guest@localhost:5672//'

	# Task result save in RabbitMQ
	CELERY_RESULT_BACKEND = "amqp"

	# Result disimpan dalam database
	# CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
	CELERY_RESULT_PERSISTENT = True

	# Membuat periodic task dari database
	CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

	# Peiodic task example to run helo_task task every minute
	CELERYBEAT_SCHEDULE = {
		'every-minute': {
			'task': 'peber_web.tasks.helo_task',
			'schedule': crontab(),  # Run every minute
			'args': ("Anwar",),  # Argumen harus berupa list atau tuple
		},
		'all-ns-harvesting': {
			'task': 'peber_web.tasks.execute_parser_by_category',
			'schedule': crontab(minute='*/30'),  # Berjalan setiap 30 menit
			'args': ("ALL",),  # ALL: Semua sumber berita, news_category: b'dasarkan kategory, dan pub:news_category
		},
	}


# Optional configuration, see the application user guide.
app.conf.update(
	CELERY_TASK_RESULT_EXPIRES=3600,
)

# app.conf.update(
# 	CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler',
# )

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object(Config)  # Langsung dari setting.py (django.conf:settings)
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
	print('Request: {0!r}'.format(self.request))


if __name__ == '__main__':
	app.start()
