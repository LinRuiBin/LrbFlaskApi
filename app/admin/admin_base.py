"""
集成flask-login 只有管理员能操作后台系统
修改默认admin样式
"""

import os

from flask import Flask, url_for, redirect, render_template, request
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import form, fields, validators
import flask_login as login
from flask_admin.contrib import sqla
import flask_admin as admin
from flask_admin import helpers, expose

from app.models import user
from app.models.base import db

#主管理员 2 副管理员 3
class AdminUser(user.User):
    # is_active is_authenticated  is_anonymous  get_id 为flask login需要
    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True if self.auth == 2 or self.auth == 3 else False

    @property
    def is_superuser(self):
        return True if self.auth == 2 else False

    @property
    def is_assituser(self):
        return True if self.auth == 3 else False

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

class LoginForm(form.Form):
    login = fields.StringField(validators=[validators.required()],label='邮箱',)
    password = fields.PasswordField(validators=[validators.required()],label='密码')



    def validate_login(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError('用户不存在')

        # we're comparing the plaintext pw with the the hash from the db
        if not check_password_hash(user.password, self.password.data):
        # to compare plain text passwords use
        # if user.password != self.password.data:
            raise validators.ValidationError('用户名或密码错误')

        if user.auth != 2 and user.auth != 3:
            raise validators.ValidationError('没有权限')

    def get_user(self):
        return db.session.query(AdminUser).filter_by(email=self.login.data).first()


# Create customized model view class
class MyModelView(sqla.ModelView):

    def is_accessible(self):
        return login.current_user.is_authenticated


# Create customized index view class that handles login & registration
class MyAdminIndexView(admin.AdminIndexView):

    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))
        return super(MyAdminIndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        # handle user login
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login.login_user(user)

        if login.current_user.is_authenticated:
            return redirect(url_for('.index'))
        self._template_args['form'] = form
        return super(MyAdminIndexView, self).index()

    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('.index'))


# Initialize flask-login
def init_login(app):
    login_manager = login.LoginManager()
    login_manager.init_app(app)

    # Create user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(AdminUser).get(user_id)
