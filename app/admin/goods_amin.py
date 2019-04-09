from app.models.goods import *
from app.admin.admin_base import MyModelView
from app.libs.ossupload import uploadpdf
from jinja2 import Markup
from wtforms import fields, widgets
from flask_admin.contrib.sqla.ajax import QueryAjaxModelLoader,DEFAULT_PAGE_SIZE
from flask_admin.model.form import InlineFormAdmin
from flask_admin import Admin, form
from wtforms.validators import ValidationError
import operator
from flask import request

#分类
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
        super(Light_CategoryAdmin, self).__init__(Light_Category, session,name='照明分类管理')

#其他分类
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


#中间表 产品-分类
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
        super(Ligh_Spu_Other_CategoryAdmin, self).__init__(Light_Spu_category, session,name='灯饰-其他分类对应关系')


# 内联pdf显示格式
class InlineModelForm(InlineFormAdmin):
    # form_excluded_columns = ('path',)
    form_label = 'PDF'
    form_columns = ('id','time','path')

    form_args = {
        'time': {
            'label': '更新时间',
        },
        'path': {
            'label': '存储路径' ,
        }
    }

    def __init__(self):
        return super(InlineModelForm, self).__init__(Light_Spu_Statement)

    def postprocess_form(self, form_class):
        form_class.upload = fields.FileField('PDF')
        return form_class

    def on_model_change(self, form, model):
        name = form.upload.name
        file_data = request.files.get(form.upload.name)

        if file_data:
           url = uploadpdf(file_data)
           model.path = url


#产品 spu
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
        'pdfs',
    ]

    column_labels = {
        'name': '灯饰名称' ,
        'spu_name': '编码' ,
        'desc':"描述",
        "category":"照明分类",
        "other_categories":"其他分类",
        "spu_num":"灯饰编码",
        'specs':"拥有规格",
        'pdfs':"pdf说明书",
    }

    def _havepdf(view, context, model, name):
        if not model.pdfs:
            return 'NO'
        return 'YES'

    column_formatters = {
        'pdfs': _havepdf
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

    inline_models = [InlineModelForm()]
    def __init__(self , session):
        # Just call parent class with predefined model.
        super(Ligh_Spu_Admin , self).__init__(Light_Spu , session , name='spu管理')



#pdf管理
class Pdf_Statement_Admin(MyModelView):
    column_display_pk = False
    column_default_sort = ('id' , True)

    column_list = [
        'time',
        'spu',
        'path' ,
    ]

    column_labels = {
        'time': '更新时间' ,
        "path": "pdf路径",
        'spu':'所属产品',
    }

    form_columns = [
        'time',
        'spu',
        'path',
    ]

    column_searchable_list = [
        'spu.name'
    ]

    column_sortable_list = ['time']


    form_extra_fields = {
        'path': fields.FileField('PDF')
    }

    def on_model_change(self, form, model, is_created):
        file_data = request.files.get(form.path.name)
        # spu = form.spu.data
        # pdfs = spu.specs
        # if spu and pdfs:
        #     raise ValidationError(message='当前产品已经有说明书')

        if file_data:
            url = uploadpdf(file_data)
            model.path = url

    def __init__(self , session):
        # Just call parent class with predefined model.
        super(Pdf_Statement_Admin , self).__init__(Light_Spu_Statement , session , name='pdf说明书管理')


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


    def __init__(self , session):
        # Just call parent class with predefined model.
        super(Ligh_Spec_Admin , self).__init__(Light_Spec , session , name='规格种类管理')

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
        super(Ligh_Spec_value_Admin , self).__init__(Light_Spec_Value , session , name='规格具体值管理')


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

    def __init__(self , session):
        # Just call parent class with predefined model.
        super(Ligh_Sku_Admin , self).__init__(Light_Sku , session , name='sku管理')