from celery import Celery

my_celery = Celery('celery_app',
include=['app.celery.tasks'])

my_celery.config_from_object("app.config.celery_config")
