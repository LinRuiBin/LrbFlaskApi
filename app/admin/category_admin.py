from app.models.goods import *
from app.admin.admin_base import MyModelView
from wtforms import fields, widgets
from flask_admin.contrib.sqla.ajax import QueryAjaxModelLoader,DEFAULT_PAGE_SIZE
from flask_admin.model.form import InlineFormAdmin
from flask_admin import Admin, form
from wtforms.validators import ValidationError
import operator
from flask import request
from app import app

#内连子分类
class CategoryInlineModelForm(InlineFormAdmin):
    # form_excluded_columns = ('path',)
    form_label = '子分类'
    form_columns = ('id','name','code','desc','is_leaf')

    form_args = {
        'name': {
            'label': '分类名称',
        },
        'code': {
            'label': '分类编码' ,
        },
        'desc': {
            'label': '分类描述',
        },
        'is_leaf': {
            'label': '是否叶子节点',
        }
    }

    def on_model_change(self, form, model, is_created):
        if model.par_cat:
            if model.par_cat.is_leaf == True:
                raise ValidationError(message="叶子分类不能创建子分类")
            model.level = model.par_cat.level + 1

    def __init__(self):
        return super(CategoryInlineModelForm, self).__init__(Light_Category)

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
        'par_cat',
        'level',
        'is_leaf',
    ]

    column_labels = {
     'id':'id',
     'name':'分类名',
     'code':'分类编码',
     'desc':'分类描述',
     'par_cat':'父分类',
     'level':'分类层级',
     'is_leaf':'是否叶子分类',
     'par_cat.name':'父分类名称',
    }

    form_columns = {
        'name': '分类名' ,
        'code': '分类编码' ,
        'desc': '分类描述' ,
        'par_cat': '父分类',
        'level': '分类层级',
        'is_leaf': '是否叶子分类',
    }

    column_searchable_list = [
        'name','code','par_cat.name',
    ]

    inline_models = [CategoryInlineModelForm(),]

    column_filters = ['name', 'code', 'par_cat.name', 'level','is_leaf']

    def create_form(self):
        return self._use_filtered_parent(
            super(Light_CategoryAdmin, self).create_form()
        )

    def edit_form(self, obj):
        return self._use_filtered_parent(
            super(Light_CategoryAdmin, self).edit_form(obj)
        )

    def _use_filtered_parent(self, form):
        form.par_cat.query_factory = self._get_parent_list
        return form

    def _get_parent_list(self):
        # only show available pets in the form
        return Light_Category.query.filter_by(is_leaf=False).all()

    def on_model_change(self, form, model, is_created):
        if  model.par_cat:
             model.level = model.par_cat.level + 1

    def __init__(self, session,category=None):
        # Just call parent class with predefined model.
        super(Light_CategoryAdmin, self).__init__(Light_Category, session,name='分类管理',category=category)

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

    def __init__(self, session,category=None):
        # Just call parent class with predefined model.
        super(Ligh_Other_CategoryAdmin, self).__init__(Light_other_Category, session,name='其他分类管理',category=category)


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
     'spu_name':'产品',
    }

    def __init__(self, session,category=None):
        # Just call parent class with predefined model.
        super(Ligh_Spu_Other_CategoryAdmin, self).__init__(Light_Spu_category, session,name='产品-其他分类对应关系',category=category)

