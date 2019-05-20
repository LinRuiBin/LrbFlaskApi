from celery import Celery

my_celery = Celery('celery_app',
broker='redis://localhost:6379/1',
backend='redis://localhost:6379/1',
include=['app.celery.tasks'])

my_celery.config_from_object("app.config.celery_config")
