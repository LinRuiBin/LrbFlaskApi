"""
 Created by LRB on 2018/5/7.
"""
from .app import Flask
from flask_script import Manager
from app.models.base import db
from app.libs.scheduler import scheduler
from app.celery import my_celery
from flask_cache import Cache
from app.config import secure
import redis
from flask_limiter import Limiter, HEADERS  # https://github.com/alisaifee/flask-limiter
from flask_limiter.util import get_remote_address

import os
__author__ = 'LRB'

"""
创建app 并注册db
其他插件在 common_init 中注册  包括蓝图路由 文档 admin 定时任务等
"""

app = Flask(__name__,template_folder='templates')
app.config.from_object('app.config.setting')
app.config.from_object('app.config.secure')
manager = Manager(app)
db.init_app(app)  #mysql 数据库 orm
redis_db = redis.Redis(host=secure.REDIS_HOST,port=secure.REDIS_PORT,password=secure.REDIS_PWD,db=3) #redis数据库初始化
#celery 异步任务 定时任务
def make_celery(app):

    class ContextTask(my_celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    my_celery.conf.update(app.config)
    my_celery.Task = ContextTask
    return my_celery

celery = make_celery(app=app) # 异步和定时任务
cache = Cache(app=app,config=secure.REDIS) #flask-cache初始化  redis

#流量限制
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri=secure.REDIS_URL,
    headers_enabled=True  # X-RateLimit写入响应头。
)
