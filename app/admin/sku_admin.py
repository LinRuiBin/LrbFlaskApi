from app.models.goods import *
from app.admin.admin_base import MyModelView
from wtforms import fields, widgets
from flask_admin.contrib.sqla.ajax import QueryAjaxModelLoader,DEFAULT_PAGE_SIZE
from flask_admin.model.form import InlineFormAdmin
from flask_admin import Admin, form
from wtforms.validators import ValidationError
import operator
from flask import request

#内联 规格值显示
spec_value_inline_form_options = {
    'form_label': "规格值",
    'form_columns': ['spec_value','id'],
    'form_args': {'spec_value':{'label':'规格值'}},
    'form_extra_fields': None,
}

#规格分类
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


    def __init__(self , session,category=None):
        # Just call parent class with predefined model.
        super(Ligh_Spec_Admin , self).__init__(Light_Spec , session , name='规格种类管理',category=category)

#规格值
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
        'spec.spec_name': '规格名称',
    }

    form_columns = [
        'spec_value' ,
        'spec' ,
    ]

    column_searchable_list = [
        'spec_value' , 'spec.spec_name'
    ]
    column_filters = ['spec_value' , 'spec.spec_name']


    def __init__(self , session,category=None):
        # Just call parent class with predefined model.
        super(Ligh_Spec_value_Admin , self).__init__(Light_Spec_Value , session , name='规格具体值管理',category=category)


#无效 ajax外健
class spec_valuesAjaxModelLoader(QueryAjaxModelLoader):
    def get_list(self , term , offset=0 , limit=10):
        query = self.session.query(self.model).filter_by(mid=term)
        return query.offset(offset).limit(limit).all()


#sku
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
        'spu.specs',
    ]

    column_labels = {
        'sku_num': 'sku编码' ,
        'sku_name': 'sku名称' ,
        'price':'价格',
        'stock':'库存',
        'spu':'所属spu',
        'spec_values':'规格值',
        'spu.specs':'拥有规格种类',
        'spu.name': 'spu名称',
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
    column_filters = ['sku_num', 'sku_name','spu.name','stock',]
    form_ajax_refs = {'spec_values':spec_valuesAjaxModelLoader('spec_values', db.session,Light_sku_spec,fields=['spec_value'])}

    def on_model_change(self, form, model, is_created):
        spu = form.spu.data
        spu_specs = spu.specs
        all_spec_id = []
        for spec in spu_specs:
            values = spec.values
            all_spec_id.append(spec.id)

        selected_spec_values = form.spec_values.data
        selected_spec_id = []
        for sel_spec_val in selected_spec_values:
            selected_spec_id.append(sel_spec_val.spec.id)

        all_spec_id.sort()
        selected_spec_id.sort()
        # 1判断规格是否 和 商品对应的规格一样
        # 2.判断统一规格是否多选
        if not len(selected_spec_id) == len(set(selected_spec_id)):
            raise ValidationError(message='同一规格重复选择')

        if not operator.eq(all_spec_id , selected_spec_id):
            raise ValidationError(message='规格值选择不正确')

        if not model.sku_name:
            model.sku_name = spu.name

    def __init__(self , session,category=None):
        # Just call parent class with predefined model.
        super(Ligh_Sku_Admin , self).__init__(Light_Sku , session , name='多规格产品管理(sku)',category=category)