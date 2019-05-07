"""
 Created by LRB on 2018/5/1.
"""
__author__ = 'LRB'


from app import app
import app_register
from app.models.base import db
from app.models.user import User

with app.app_context():
    with db.auto_commit():
        # 创建一个超级管理员
        user = User()
        user.nickname = 'Super'
        user.password = '123456'
        user.email = '18675079557@163.com'
        user.auth = 2
        db.session.add(user)
