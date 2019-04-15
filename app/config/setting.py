"""
 Created by LRB on 2018/5/7.
"""

__author__ = 'LRB'


# TOKEN_EXPIRATION = 30 * 24 * 3600
TOKEN_EXPIRATION = 60 * 2

DEBUG = False
API_DOC_ENABLE = DEBUG
BABEL_DEFAULT_LOCALE = 'zh_CN'
SQLALCHEMY_TRACK_MODIFICATIONS = True
PAGE_SIZE = 20
PAGE_DISPLAY = 20
RELEASE_VERSION = '1.0.0'

UPLOAD = {
    'ext':[ 'jpg','gif','bmp','jpeg','png' ],
    'prefix_path':'/static/upload/',
    'prefix_url':'/static/upload/'
}

APP = {
    'domain':'https://lruibin.top/'
}
