from app.models.user import User
from app.admin.admin_base import MyModelView
import flask_login as login
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import PasswordField,StringField

class UserAdmin(MyModelView):
    print()
    action_disallowed_list = ['delete']
    column_display_pk = True
    can_delete = False
    can_create = True
    can_export = True

    column_list = [
        # 'id',
        'email',
        'nickname',
        'auth',
        'phone',
    ]

    column_default_sort = ('id',True)
    column_searchable_list = [
        'id',
        'email',
        'nickname',
        'phone',
    ]

    column_filters = [
        'email',
        'nickname',
        'phone',
    ]

    column_labels = {
        'id': 'id',
        'email': '邮箱',
        'nickname': '昵称',
        'auth': '权限',
        'phone': '电话',
        'status': '状态',
        'gender':"性别",
        'avatar':"头像",
        'create_time':"注册时间",
        'password':"密码",
    }

    form_columns = {
        'email': '邮箱' ,
        'nickname': '昵称' ,
        'auth': '权限' ,
        'phone': '电话' ,
        'status': '状态' ,
        'gender': "性别" ,
        'avatar': "头像" ,
        'password': "头像" ,
    }

    column_choices = {
        'auth': [
            (1 , '普通用户'),
            (2 , '管理员'),
            (3 , '副管理员'),
        ],
        'gender': [
            (0 , '男') ,
            (1 , '女') ,
        ],
        'status': [
            (0 , '删除') ,
            (1 , '正常') ,
        ],
    }

    form_choices = {
        'auth': [
            ('1' , '普通用户'),
            ('2' , '管理员'),
            ('3' , '副管理员'),
        ],
        'gender': [
            ('0' , '男'),
            ('1' , '女'),
        ],
        'status': [
            ('0' , '删除'),
            ('1' , '正常'),
        ],
    }

    form_extra_fields = {
        'password': StringField(label='密码')
     }

    def on_model_change(self, form, User, is_created):
         User.password = form.password.data


    def is_accessible(self):
        return login.current_user.is_superuser

    def __init__(self, session):
        # Just call parent class with predefined model.
        super(UserAdmin, self).__init__(User, session,name='用户管理')



class Assit_UserAdmin(UserAdmin):
    can_export = False
    can_create = False
    can_edit = False

    def is_accessible(self):
        return login.current_user.is_assituser

    def __init__(self , session):
        # Just call parent class with predefined model.
        super(UserAdmin , self).__init__(User , session , name='用户管理',endpoint='assit_user')