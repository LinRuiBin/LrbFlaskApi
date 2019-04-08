from app.models.goods import *
from app.admin.admin_base import MyModelView
from jinja2 import Markup
from wtforms import fields, widgets
from flask_admin.contrib.sqla.ajax import QueryAjaxModelLoader,DEFAULT_PAGE_SIZE

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
        'other_categories',
        'specs',
    ]

    column_labels = {
        'name': '灯饰名称' ,
        'spu_name': '编码' ,
        'desc':"描述",
        "category":"照明分类",
        "other_categories":"其他分类",
        "spu_num":"灯饰编码",
        'specs':"拥有规格",
    }

    form_columns = [
        'name',
        'spu_num',
        'desc',
        'category',
        'other_categories',
        'specs' ,
    ]

    column_searchable_list = [
        'name' , 'spu_num','category.name','other_categories.name',
    ]


    def __init__(self , session):
        # Just call parent class with predefined model.
        super(Ligh_Spu_Admin , self).__init__(Light_Spu , session , name='灯饰spu管理')




spec_value_inline_form_options = {
    'form_label': "规格值",
    'form_columns': ['spec_value','id'],
    'form_args': {'spec_value':{'label':'规格值'}},
    'form_extra_fields': None,
}

class Ligh_Spec_Admin(MyModelView):
    column_display_pk = False
    column_default_sort = ('id' , True)

    column_list = [
        'spec_num',
        'spec_name',
        'values',
    ]

    column_labels = {
        'spec_name': '规格名称' ,
        "spec_num": "规格编码" ,
        'values':'规格值',
    }

    form_columns = [
        'spec_name' ,
        'spec_num' ,
    ]

    inline_models = [(Light_Spec_Value,spec_value_inline_form_options),]

    column_searchable_list = [
        'spec_name' , 'spec_num'
    ]


    def __init__(self , session):
        # Just call parent class with predefined model.
        super(Ligh_Spec_Admin , self).__init__(Light_Spec , session , name='灯饰规格种类管理')


class Ligh_Spec_value_Admin(MyModelView):
    column_display_pk = False
    column_default_sort = ('id' , True)

    column_list = [
        'spec_value',
        'spec',
    ]

    column_labels = {
        'spec_value': '规格具体值' ,
        "spec": "所属规格" ,
    }

    form_columns = [
        'spec_value' ,
        'spec' ,
    ]

    column_searchable_list = [
        'spec_value' , 'spec.spec_name'
    ]


    def __init__(self , session):
        # Just call parent class with predefined model.
        super(Ligh_Spec_value_Admin , self).__init__(Light_Spec_Value , session , name='灯饰规格具体值管理')



class spec_valuesAjaxModelLoader(QueryAjaxModelLoader):
    def get_list(self , term , offset=0 , limit=10):
        query = self.session.query(self.model).filter_by(mid=term)
        return query.offset(offset).limit(limit).all()



class Ligh_Sku_Admin(MyModelView):
    column_display_pk = False
    column_default_sort = ('id' , True)

    column_list = [
        'sku_num',
        'sku_name',
        'price',
        'stock',
        'spu',
        'spec_values',
    ]

    column_labels = {
        'sku_num': 'sku编码' ,
        'sku_name': 'sku名字' ,
        'price':'价格',
        'stock':'库存',
        'spu':'所属spu',
        'spec_values':'规格id',
    }

    form_columns = [
        'sku_num' ,
        'sku_name' ,
        'price',
        'stock',
        'spu',
        'spec_values',
    ]

    column_searchable_list = [
        'sku_num' , 'sku_name','spu.name',
    ]

    form_ajax_refs = {'spec_values':spec_valuesAjaxModelLoader('spec_values', db.session,Light_sku_spec,fields=['spec_value'])}

    def on_model_change(self, form, model, is_created):
        pass

    def __init__(self , session):
        # Just call parent class with predefined model.
        super(Ligh_Sku_Admin , self).__init__(Light_Sku , session , name='灯饰sku管理')