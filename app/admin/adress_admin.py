from app.models.adress import *
from app.admin.admin_base import MyModelView


class Adress_admin(MyModelView):

    column_display_pk =False
    column_default_sort = ('id',True)

    column_list = [
        'id',
        'user',
        'nickname',
        'province_str',
        'city_str',
        'area_str',
        'address',
        'is_default',
        'update_time',
    ]

    column_labels = {
     'id':'id',
     'user':'用户',
     'nickname':'收货人',
     'mobile':'手机',
     'province_str':'省份',
     'city_str':'城市',
     'area_str': '区域',
     'address': '详细地址',
     'is_default':'是否为默认地址',
     'user.nickname':'用户名',
     'province_id':'省份id',
     'city_id':'城市id',
     'area_id':'区域id',
     'update_time':'更新时间',
    }

    form_columns = [
        'user','nickname','mobile','province_str','province_id','city_str','city_id','area_str','area_id','address','is_default',
    ]

    column_searchable_list = [
        'user.nickname','nickname','mobile','address','province_str','city_str','area_str','is_default',
    ]

    column_filters = [
        'user.nickname','nickname','mobile','address','province_str','city_str','area_str','is_default',
    ]

    def _isdefault(view, context, model, name):
        if model.is_default == 1:
            return '是'
        return '否'

    column_formatters = {
        'is_default':_isdefault,
    }

    form_choices = {'is_default': [
        ('1','是'),
        ('0','否'),
    ]}

    def on_model_change(self, form, model, is_created):
        model.is_default = int(form.is_default.data)
        user = form.user.data
        if model.is_default==1 and user:
            adresss = user.adresses
            if len(adresss) > 1:
                for adrr in adresss:
                    if adrr.id != model.id:
                        adrr.is_default = 0


    def __init__(self, session,category=None):
        # Just call parent class with predefined model.
        super(Adress_admin, self).__init__(Adress, session,name='地址管理',category=category)