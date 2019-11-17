from app.models.userOrder import *
from app.admin.admin_base import MyModelView

#杜林洋定制数据项目
class User_OrderInfo_Admin(MyModelView):

    column_display_pk =False
    column_default_sort = ('id',True)

    column_display_pk = True
    column_list = [
        # 'id',
        'name',
        'study_Id',
        'order_num' ,
        'money',
        'desc',
    ]

    column_labels = {
     'id':'id',
     'name':'姓名',
     'study_Id':'学号',
     'money':'钱钱',
     'order_num':'订单号',
     'desc': '描述' ,
    }

    form_columns = {
        'name': '姓名' ,
        'study_Id': '学号' ,
        'money':'钱钱',
        'order_num': '订单号' ,
        'desc': '描述' ,
    }

    column_searchable_list = [
        'name','study_Id','order_num'
    ]

    def __init__(self, session):
        # Just call parent class with predefined model.
        super(User_OrderInfo_Admin, self).__init__(User_Order_Info, session,name='杜林洋数据管理1')