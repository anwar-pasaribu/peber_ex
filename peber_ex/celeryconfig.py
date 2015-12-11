# Setting for celery
CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json','pickle']

BROKER_URL = 'amqp://guest:guest@localhost:5672//'
# Task result save in RabbitMQ
CELERY_RESULT_BACKEND = "amqp://"

# Result disimpan dalam database
# CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
CELERY_RESULT_PERSISTENT = True

# Peiodic task example
CELERYBEAT_SCHEDULE = {
    'every-minute': {
        'task': 'peber_web.tasks.helo_task',
        'schedule': crontab(minute='*/1'),
        'args': ("Anwar"),
    },
}