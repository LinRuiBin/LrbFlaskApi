from app.models.goods import *
from app.admin.admin_base import MyModelView
from app.libs.ossupload import uploadpdf,uploadQrcode
from app.libs.helper import createQrcodeWithurl
from jinja2 import Markup
from wtforms import fields, widgets
from flask_admin.contrib.sqla.ajax import QueryAjaxModelLoader,DEFAULT_PAGE_SIZE
from flask_admin.model.form import InlineFormAdmin
from flask_admin import Admin, form
from wtforms.validators import ValidationError
import operator
from flask import request
from app import app


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
        'auto_qr',
        'qrcode',
    ]

    column_labels = {
        'name': '名称' ,
        'spu_name': '编码' ,
        'desc':"描述",
        "category":"分类",
        "other_categories":"其他分类",
        "spu_num":"编码",
        'specs':"拥有规格",
        'pdfs':"pdf说明书",
        'auto_qr':'是否生成二维码',
        'qrcode':"二维码",
        'category.name':'分类名称',
        'other_categories.name':'其他分类名称',
    }

    def _havepdf(view, context, model, name):
        if not model.pdfs:
            return 'NO'
        return 'YES'

    def _listQrcode(view, context, model, name):
        qrcodes = model.qrcode
        qrcode = None
        if qrcodes:
            qrcode = qrcodes[0]
        if not qrcode:
            return ''
        return Markup('<img src="%s" height="100" width="100">' % qrcode.path)


    def _automakeQrcode(view, context, model, name):
        if model.qrcode == True:
            return 'YES'
        return 'NO'

    column_formatters = {
        'pdfs': _havepdf,
        'qrcode':_listQrcode,
        'auto_qr': _automakeQrcode,
    }

    form_columns = [
        'name',
        'spu_num',
        'desc',
        'category',
        'other_categories',
        'specs' ,
        'qrcode',
        'auto_qr',
    ]

    column_searchable_list = [
        'name' , 'spu_num','category.name','other_categories.name',
    ]
    column_filters = ['name', 'spu_num', 'category.name', 'other_categories.name']

    inline_models = [InlineModelForm()]

    def create_form(self):
        return self._use_leaf_category(
            super(Ligh_Spu_Admin, self).create_form()
        )

    def edit_form(self, obj):
        return self._use_leaf_category(
            super(Ligh_Spu_Admin, self).edit_form(obj)
        )

    def _use_leaf_category(self, form):
        form.category.query_factory = self._get_leafcat_list
        return form

    def _get_leafcat_list(self):
        # only show available pets in the form
        return Light_Category.query.filter_by(is_leaf=True).all()

    def on_model_change(self, form, model, is_created):
        if form.auto_qr.data == False:
            return
        spu = model
        old_qrcode = spu.qrcode
        if not old_qrcode:
            spu_code = form.spu_num.data
            domain = app.config['APP']['domain']
            qrcode_url = domain + '?spu_num=' + spu_code
            new_qrcode = Light_Spu_Qrcode()
            qrcode_file = createQrcodeWithurl(qrcode_url)
            path = uploadQrcode(qrcode_file)
            new_qrcode.path = path
            new_qrcode.spu = spu
            db.session.add(new_qrcode)
            db.session.commit()


    def __init__(self , session ,category=None):
        # Just call parent class with predefined model.
        super(Ligh_Spu_Admin , self).__init__(Light_Spu , session , name='产品管理(spu)',category=category)



#pdf管理
class Pdf_Statement_Admin(MyModelView):
    column_display_pk = False
    column_default_sort = ('id' , True)
    can_edit = False
    can_export = True
    can_create = False

    column_list = [
        'time',
        'spu',
        'path' ,
    ]

    column_labels = {
        'time': '更新时间' ,
        "path": "pdf路径",
        'spu':'所属产品',
        'spu.name':'产品名称(spu)',
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
    column_filters = ['spu.name']

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

    def __init__(self , session,category=None):
        # Just call parent class with predefined model.
        super(Pdf_Statement_Admin , self).__init__(Light_Spu_Statement , session , name='PDF说明书管理',category=category)


# 二维码管理
class Qrcode_Statement_Admin(MyModelView):
    column_display_pk = False
    column_default_sort = ('id' , True)
    can_edit = False
    can_export = True
    can_create = False

    column_list = [
        'time' ,
        'spu' ,
        'path' ,
    ]

    column_labels = {
        'time': '更新时间' ,
        "path": "二维码路径" ,
        'spu': '所属产品' ,
        'spu.name':'产品(spu)名称',
    }

    form_columns = [
        'time' ,
        'spu' ,
        'path' ,
    ]

    column_searchable_list = [
        'spu.name'
    ]
    column_sortable_list = ['time']

    column_filters = ['spu.name']

    def __init__(self , session,category=None):
        # Just call parent class with predefined model.
        super(Qrcode_Statement_Admin , self).__init__(Light_Spu_Qrcode , session , name='产品二维码管理',category=category)

