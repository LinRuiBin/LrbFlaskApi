import os

from flask import Flask, url_for, redirect, render_template, request
from werkzeug.security import generate_password_hash, check_password_hash

import flask_admin as admin
from flask_admin.contrib import sqla
from wtforms import form, fields, validators
import flask_login as login
from flask_admin import helpers, expose

from app.models import user,book,gift
from app.models.base import db


class AdminUser(user.User):
    # is_active is_authenticated  is_anonymous  get_id 为flask login需要
    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True if self.auth == 2 else False

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
            raise validators.ValidationError('无用户')

        # we're comparing the plaintext pw with the the hash from the db
        if not check_password_hash(user.password, self.password.data):
        # to compare plain text passwords use
        # if user.password != self.password.data:
            raise validators.ValidationError('用户名或密码错误')

        if user.auth != 2:
            raise validators.ValidationError('没有管理员权限')

    def get_user(self):
        return db.session.query(AdminUser).filter_by(email=self.login.data).first()


# Initialize flask-login
def init_login(app):
    login_manager = login.LoginManager()
    login_manager.init_app(app)

    # Create user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(AdminUser).get(user_id)


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


def init_admin(app):
    init_login(app)
    #  template_mode='bootstrap3',
    fadmin = admin.Admin(app, name='lrb管理后台',template_mode='bootstrap3',index_view=MyAdminIndexView(), base_template='admin/my_master.html')
    fadmin.add_view(MyModelView(user.User,db.session))
    fadmin.add_view(MyModelView(book.Book, db.session))
    fadmin.add_view(MyModelView(gift.Gift, db.session))


