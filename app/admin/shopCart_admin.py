from app.models.shopCart import *
from app.admin.admin_base import MyModelView


class ShopCart_admin(MyModelView):

    column_display_pk =False
    column_default_sort = ('id',True)

    column_list = [
        'id',
        'user',
        'sku',
        'quantity',
        'update_time',
    ]

    column_labels = {
     'id':'id',
     'user':'用户',
     'user.nickname':'用户名',
     'sku':'商品',
     'quantity':'数量',
     'update_time':'更新时间',
     'sku.sku_name':'商品名称',
    }

    form_columns = [
        'user','sku','quantity',
    ]

    column_searchable_list = [
        'user.nickname','sku.sku_name',
    ]

    column_filters = [
        'user.nickname', 'sku.sku_name',
    ]

    def __init__(self, session,category=None):
        # Just call parent class with predefined model.
        super(ShopCart_admin, self).__init__(ShopCart, session,name='购物车管理',category=category)