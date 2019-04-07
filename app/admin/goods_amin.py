from app.models.goods import *
from app.admin.admin_base import MyModelView
from jinja2 import Markup
from wtforms import fields, widgets

class Light_CategoryAdmin(MyModelView):

    column_display_pk =False
    column_default_sort = ('id',True)

    column_display_pk = True
    column_list = [
        'id',
        'name',
        'code',
        'desc',
    ]

    column_labels = {
     'id':'id',
     'name':'分类名',
     'code':'分类编码',
     'desc':'分类描述',
    }

    form_columns = {
        'name': '分类名' ,
        'code': '分类编码' ,
        'desc': '分类描述' ,
    }

    column_searchable_list = [
        'name','code',
    ]

    def __init__(self, session):
        # Just call parent class with predefined model.
        super(Light_CategoryAdmin, self).__init__(Light_Category, session,name='灯饰照明分类管理')


class Ligh_Other_CategoryAdmin(MyModelView):

    column_display_pk =False
    column_default_sort = ('id',True)

    column_display_pk = True
    column_list = [
        'id',
        'name',
        'code',
        'desc',
    ]

    column_labels = {
     'id':'id',
     'name':'分类名',
     'code':'分类编码',
     'desc':'分类描述',
    }

    form_columns = {
        'name': '分类名' ,
        'code': '分类编码' ,
        'desc': '分类描述' ,
    }

    column_searchable_list = [
        'name','code',
    ]

    def __init__(self, session):
        # Just call parent class with predefined model.
        super(Ligh_Other_CategoryAdmin, self).__init__(Light_other_Category, session,name='其他分类管理')



class Ligh_Spu_Other_CategoryAdmin(MyModelView):

    column_display_pk =False
    column_default_sort = ('id',True)
    can_create = False
    can_edit = False

    column_display_pk = True
    column_list = [
        'other_category_name',
        'spu_name',
    ]

    column_labels = {
     'other_category_name':'分类',
     'spu_name':'灯饰',
    }

    def __init__(self, session):
        # Just call parent class with predefined model.
        super(Ligh_Spu_Other_CategoryAdmin, self).__init__(Light_Spu_category, session,name='灯饰-其他分类管理')



class Ligh_Spu_Admin(MyModelView):
    column_display_pk = False
    column_default_sort = ('id' , True)

    column_list = [
        'name',
        'spu_num',
        'desc',
        'category',
        'other_categories'
    ]

    column_labels = {
        'name': '灯饰名称' ,
        'spu_name': '编码' ,
        'desc':"描述",
        "category":"照明分类",
        "other_categories":"其他分类",
        "spu_num":"灯饰编码",
    }

    form_columns = [
        'name',
        'spu_num',
        'desc',
        'category',
        'other_categories',
    ]

    column_searchable_list = [
        'name' , 'spu_num','category.name','other_categories.name',
    ]


    def __init__(self , session):
        # Just call parent class with predefined model.
        super(Ligh_Spu_Admin , self).__init__(Light_Spu , session , name='灯饰spu管理')