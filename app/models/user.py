"""
 Created by LRB on 2018/5/7.

"""
from sqlalchemy import inspect, Column, Integer, String, SmallInteger, orm
from werkzeug.security import generate_password_hash, check_password_hash

from app.libs.error_code import NotFound, AuthFailed
from app.models.base import Base, db, MixinJSONSerializer
import datetime

from flask import current_app

import requests,json

__author__ = 'LRB'

class User(Base):
    id = Column(Integer, primary_key=True)
    email = Column(String(24), unique=True,index=True)
    nickname = Column(String(24))
    auth = Column(SmallInteger, default=1) #权限 1 为普通用户 2 为管理员
    phone = Column(String(24), unique=True,index=True)
    avatar = Column(String(200))
    gender = Column(Integer)
    _password = Column('password', String(100))

    def keys(self):
        return ['id', 'email', 'nickname', 'auth','avater','gender']

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    @staticmethod
    def register_by_email(nickname, account, secret):
        with db.auto_commit():
            user = User()
            user.nickname = nickname
            user.email = account
            user.password = secret
            db.session.add(user)

    @staticmethod
    def verify(email, password):
        user = User.query.filter_by(email=email).first_or_404()
        if not user.check_password(password):
            raise AuthFailed()
        scope = 'AdminScope' if user.auth == 2 else 'UserScope'
        return {'uid': user.id, 'scope': scope}

    @property
    def scope(self):
        return 'AdminScope' if self.auth == 2 else 'UserScope'

    def check_password(self, raw):
        if not self._password:
            return False
        return check_password_hash(self._password, raw)


        # def _set_fields(self):
    #     # self._exclude = ['_password']
    #     self._fields = ['_password', 'nickname']


class OauthMemberBind(Base):

    __tablename__ = 'oauth_member_bind'
    __table_args__ = (
        db.Index('idx_openid_type', 'type', 'openid'),  # 联合索引
    )
    id = Column(Integer, primary_key=True)
    user = db.relationship(User, backref='oauthBind')
    user_id = Column(Integer,db.ForeignKey(User.id),nullable=False)
    client_type = Column(db.String(20))
    type = Column(Integer, nullable=False)
    openid = Column(String(80), nullable=False,unique=True)
    unionid = Column(String(100))
    extra = Column(String(200))

    @staticmethod
    def getWeChatOpenId(code):
        url = "https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code" \
            .format(current_app.config['MINA_APP']['appid'] , current_app.config['MINA_APP']['appkey'] , code)
        r = requests.get(url)
        res = json.loads(r.text)
        openid = None
        if 'openid' in res:
            openid = res['openid']
        return openid