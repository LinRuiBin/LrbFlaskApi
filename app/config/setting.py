"""
 Created by LRB on 2018/5/7.
"""

__author__ = 'LRB'


TOKEN_EXPIRATION = 30 * 24 * 3600  #测试 延长token
#TOKEN_EXPIRATION = 60 * 2

DEBUG = True
API_DOC_ENABLE = DEBUG
BABEL_DEFAULT_LOCALE = 'zh_CN'
SQLALCHEMY_TRACK_MODIFICATIONS = True
PAGE_SIZE = 20
PAGE_DISPLAY = 20
RELEASE_VERSION = '1.0.0'
SCHEDULER_API_ENABLED = True
CELERY_BROKER_URL = 'redis://localhost:6379/1'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'

UPLOAD = {
    'ext':[ 'jpg','gif','bmp','jpeg','png' ],
    'prefix_path':'/static/upload/',
    'prefix_url':'/static/upload/'
}

APP = {
    'domain':'https://lruibin.top/'
}


PAY_STATUS_MAPPING = {
    "1":"已支付",
    "-8":"待支付",
    "0":"已关闭"
}

PAY_STATUS_DISPLAY_MAPPING = {
    "0":"订单关闭",
    "1":"支付成功",
    "-8":"待支付",
    "-7":"待发货",
    "-6":"待确认",
    "-5":"待评价"
}
