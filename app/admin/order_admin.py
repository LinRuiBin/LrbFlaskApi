from app.models.order import *
from app.admin.admin_base import MyModelView

class Order_admin(MyModelView):

    column_display_pk = True
    column_default_sort = ('id',True)
    can_delete = False
    column_list = [
        'id',
        'order_sn',
        'user',
        'total_price',
        'pay_price',
        'yun_price',
        'pay_sn',
        'prepay_id',
        'note',
        'order_status',
        'express_address',
        'express_status',
        'express_info',
        'comment_status',
        'pay_time',
        'create_time',
        'update_time',
    ]

    column_labels = {
     'id':'id',
     'user':'用户',
     'user.nickname':'用户名',
     'total_price':'总金额',
     'yun_price':'运费',
     'pay_price':'实际支付金额',
     'order_sn':'订单号',
     'pay_sn':'支付单号',
     'prepay_id':'预支付id',
     'order_status':'订单状态',
     'express_address':'快递地址',
     'express_status':'快递状态',
     'express_info':'快递信息',
     'comment_status':'评论状态',
     'pay_time':'支付时间',
     'create_time':'创建时间',
     'update_time':'更新时间',
     'note':'备注',
    }

    form_columns = [
        'order_sn',
        'user',
        'total_price',
        'pay_price',
        'yun_price',
        'pay_sn',
        'prepay_id',
        'note',
        'order_status',
        'express_address',
        'express_status',
        'express_info',
        'comment_status',
        'pay_time',
    ]

    column_searchable_list = [
        'user.nickname','order_sn','order_status','express_status','order_sn',
    ]

    column_filters = [
        'user.nickname','order_status','express_status','create_time','update_time','pay_time','pay_price','total_price',
    ]

    def __init__(self, session,category=None):
        # Just call parent class with predefined model.
        super(Order_admin, self).__init__(PayOrder, session,name='订单管理',category=category)