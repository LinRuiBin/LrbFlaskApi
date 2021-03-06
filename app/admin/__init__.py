import os

import flask_admin as admin
from app.models.base import db
from app.admin.admin_base import MyAdminIndexView
from app.admin.user_admin import UserAdmin,Assit_UserAdmin

from app.admin.goods_amin import *
from app.admin.sku_admin import *
from app.admin.category_admin import *
from app.admin.adress_admin import *
from app.admin.shopCart_admin import *
from app.admin.order_admin import *
from app.admin.order_admin import *
from app.admin.user_order_Info_admin import *

def init_admin(app):
    admin_base.init_login(app)
    #  template_mode='bootstrap3',
    fadmin = admin.Admin(app, name='lrb管理后台', template_mode='bootstrap3', index_view=MyAdminIndexView(), base_template='admin/my_master.html',endpoint='admin')
    fadmin.add_view(UserAdmin(db.session))
    fadmin.add_view(Assit_UserAdmin(db.session))
    # fadmin.add_view(Ligh_Spu_Admin(db.session))
    # fadmin.add_view(Ligh_Sku_Admin(db.session))
    # fadmin.add_view(Qrcode_Statement_Admin(db.session))
    # fadmin.add_view(Pdf_Statement_Admin(db.session))
    # fadmin.add_view(Light_CategoryAdmin(db.session))
    # fadmin.add_view(Ligh_Other_CategoryAdmin(db.session))
    # # fadmin.add_view(Ligh_Spu_Other_CategoryAdmin(db.session))
    # fadmin.add_view(Ligh_Spec_Admin(db.session))
    # fadmin.add_view(Ligh_Spec_value_Admin(db.session))
    # fadmin.add_view(Adress_admin(db.session))
    # fadmin.add_view(ShopCart_admin(db.session))
    # fadmin.add_view(Order_admin(db.session))
    # fadmin.add_view(Order_item_admin(db.session))
    fadmin.add_view(User_OrderInfo_Admin(db.session))