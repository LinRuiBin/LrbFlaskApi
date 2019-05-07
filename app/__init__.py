"""
 Created by LRB on 2018/5/7.
"""
from .app import Flask
from flask_script import Manager
from app.models.base import db

import os
__author__ = 'LRB'

"""
创建app 并注册db
其他插件在 app_register 中注册  包括蓝图路由 文档 admin等
"""

app = Flask(__name__,template_folder='templates')
app.config.from_object('app.config.setting')
app.config.from_object('app.config.secure')
manager = Manager(app)
db.init_app(app)