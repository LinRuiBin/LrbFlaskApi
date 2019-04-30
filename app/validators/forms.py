"""
 Created by LRB on 2018/5/10.
"""
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, length, Email, Regexp
from wtforms import ValidationError

from app.libs.enums import ClientTypeEnum
from app.models.user import User
from app.validators.base import BaseForm as Form
from app.models.base import db
from app.libs.error_code import RegisteredException,NotRegisteredException
__author__ = 'LRB'


class ClientForm(Form):
    account = StringField(validators=[DataRequired(message='不允许为空'), length(
        min=5, max=32
    )])
    secret = StringField()
    type = IntegerField(validators=[DataRequired()])

    def validate_type(self, value):
        try:
            if (isinstance(value.data,str)):
                value.data = int(value.data)
            client = ClientTypeEnum(int(value.data))
        except ValueError as e:
            raise e
        self.type.data = client

    def validate_account(self, value):
        user = User.query.filter_by(email=value.data).first()
        if user:
            raise RegisteredException()



class EmailLoginForm(Form):
    account = StringField(validators=[DataRequired(message='不允许为空'), length(
        min=5, max=32
    )])
    secret = StringField()
    type = IntegerField(validators=[DataRequired()])

    def validate_type(self, value):
        try:
            if (isinstance(value.data, str)):
                value.data = int(value.data)
            client = ClientTypeEnum(int(value.data))
        except ValueError as e:
            raise e
        self.type.data = client

    def validate_account(self, value):
        user = User.query.filter_by(email=value.data).first()
        if not user:
            raise NotRegisteredException()



# 微信登录 注册
class WxClientForm(Form):
    code=StringField(validators=[DataRequired()])
    type=IntegerField(validators=[DataRequired()]) #微信小程序type 200
    def validate_type(self, value):
        try:
            if (isinstance(value.data,str)):
                value.data = int(value.data)
            client = ClientTypeEnum(int(value.data))
        except ValueError as e:
            raise e
        self.type.data = client


class UserEmailForm(ClientForm):
    account = StringField(validators=[
        Email(message='invalidate email')
    ])
    secret = StringField(validators=[
        DataRequired(),
        # password can only include letters , numbers and "_"
        Regexp(r'^[A-Za-z0-9_*&$#@]{6,22}$')
    ])
    nickname = StringField(validators=[DataRequired(),
                                       length(min=2, max=22)])

    def validate_account(self, value):
        if User.query.filter_by(email=value.data).first():
            raise ValidationError()


class BookSearchForm(Form):
    q = StringField(validators=[DataRequired(message="搜索参数不能为空")])


class TokenForm(Form):
    token = StringField(validators=[DataRequired()])
