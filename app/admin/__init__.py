import os

import flask_admin as admin
from app.models.base import db
from app.admin.admin_base import MyAdminIndexView
from app.admin.user_admin import UserAdmin,Assit_UserAdmin
from app.admin.book_admin import BookAdmin
from app.admin.gitf_amin import GiftAdmin
from app.admin.goods_amin import *

def init_admin(app):
    admin_base.init_login(app)
    #  template_mode='bootstrap3',
    fadmin = admin.Admin(app, name='lrb管理后台', template_mode='bootstrap3', index_view=MyAdminIndexView(), base_template='admin/my_master.html',endpoint='admin')
    fadmin.add_view(UserAdmin(db.session))
    fadmin.add_view(Assit_UserAdmin(db.session))
    # fadmin.add_view(BookAdmin(db.session))
    fadmin.add_view(Light_CategoryAdmin(db.session))
    fadmin.add_view(Ligh_Other_CategoryAdmin(db.session))
    fadmin.add_view(Ligh_Spu_Other_CategoryAdmin(db.session))
    fadmin.add_view(Ligh_Spu_Admin(db.session))
    fadmin.add_view(Ligh_Spec_Admin(db.session))
    fadmin.add_view(Ligh_Spec_value_Admin(db.session))
    fadmin.add_view(Ligh_Sku_Admin(db.session))
    fadmin.add_view(Pdf_Statement_Admin(db.session))

    # fadmin.add_view(GiftAdmin())

