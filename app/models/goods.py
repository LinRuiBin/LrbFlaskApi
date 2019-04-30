from sqlalchemy import inspect, Column, Integer, String, SmallInteger, orm
from app.libs.error_code import NotFound, AuthFailed
from app.models.base import Base, db, MixinJSONSerializer
from sqlalchemy.ext.associationproxy import association_proxy
from datetime import datetime


#多对一 照明分类
class Light_Category(Base):
    __tablename__ = 'light_category'
    id = Column(db.Integer , primary_key=True , autoincrement=True)
    par_id = db.Column(db.Integer , db.ForeignKey('light_category.id'))
    par_cat = db.relationship('Light_Category',backref=db.backref("sub_cats"),remote_side=[id])
    level = Column(db.Integer, nullable = False, default = 0) #分类层级 0代表根分类
    is_leaf = Column(db.Boolean,default=False) #是否子节点
    name = Column(db.String(50) , nullable=False)
    code = Column(db.String(20),unique=True)  #分类编码
    desc = Column(db.String(50), nullable=True)

    def __str__(self):
        return "{}".format(self.name)

    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'name', 'code', 'desc',]

#灯其他分类  多对多
class Light_other_Category(Base):
    __tablename__ = 'light_other_category'
    id = Column(db.Integer , primary_key=True)
    name = Column(db.String(50) , nullable=False)
    code = Column(db.String(20),unique=True)  #分类编码
    desc = Column(db.String(50), nullable=True)

    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'name', 'code', 'desc',]

    def __str__(self):
        return "{}".format(self.name)

#灯其他分类 中间表
class Light_Spu_category(db.Model):

    __tablename__ = 'light_spu_category'
    id = Column(db.Integer , primary_key=True)
    spu_id = db.Column(db.Integer , db.ForeignKey('light_spu.id'),primary_key=True)
    other_category_id = db.Column(db.Integer , db.ForeignKey('light_other_category.id'),primary_key=True)
    other_category = db.relationship(Light_other_Category , backref=db.backref("other_spu_categorys"))
    other_category_name = association_proxy('other_category' , 'name')
    light_spu = db.relationship('Light_Spu' , backref=db.backref("spu_other_categorys",cascade="all, delete-orphan"))
    spu_name = association_proxy('light_spu' , 'name')

    def __init__(self, light_other_category=None, light_spu=None):
        self.other_category = light_other_category
        self.light_spu = light_spu

#灯spu
class Light_Spu(Base):
    __tablename__ = 'light_spu'
    id = Column(db.Integer , primary_key=True)
    name = Column(db.String(50) ,nullable=False)
    spu_num = Column(db.String(50), unique=True,nullable=False,index=True)  # 商品编码
    desc = Column(db.String(50) , nullable=True)
    category_id = Column(db.Integer,db.ForeignKey('light_category.id'))
    category = db.relationship(Light_Category , backref='lights')
    other_categories = association_proxy("spu_other_categorys",'other_category')
    specs = association_proxy('spu_specs','spec')
    auto_qr = Column(db.Boolean,default=False)

    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'name', 'spu_num', 'desc','category','other_categories','spu_skus',]

    def __str__(self):
        return "{}".format(self.name)


# 产品二维码
class Light_Spu_Qrcode(Base):
    __tablename__ = 'light_spu_qrcode'
    id = Column(db.Integer , primary_key=True)
    time = Column(db.DateTime , default=datetime.now , onupdate=datetime.now)
    path = Column(db.String(100))
    spu_id = Column(db.Integer, db.ForeignKey('light_spu.id'))
    spu = db.relationship(Light_Spu , backref='qrcode',uselist=False)

    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'path','time']


#产品说明书 pdf
class Light_Spu_Statement(Base):
    __tablename__ = 'light_spu_statement'
    id = Column(db.Integer , primary_key=True)
    time = Column(db.DateTime,default=datetime.now,onupdate=datetime.now)
    path = Column(db.String(100))
    spu_id = Column(db.Integer,db.ForeignKey('light_spu.id'))
    spu = db.relationship(Light_Spu , backref='pdfs')

    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'path','time']


#规格表
class Light_Spec(Base):
    __tablename__ = 'light_spec'
    id = Column(db.Integer , primary_key=True)
    spec_num = Column(db.String(50) , unique=True,nullable=False)  # 规格编码
    spec_name = Column(db.String(50) , unique=True,nullable=False) #规格名称

    def __str__(self):
        return "{}".format(self.spec_name)

    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'spec_num', 'spec_name']


#规格值表
class Light_Spec_Value(Base):
    __tablename__ = 'light_spec_value'
    id = Column(db.Integer , primary_key=True)
    spec_id = Column(db.Integer,db.ForeignKey('light_spec.id'))  # 规格id
    spec = db.relationship(Light_Spec,backref='values')
    spec_value =  Column(db.String(50) , unique=True,nullable=False) #规格值

    def __str__(self):
        return "{}".format(self.spec_value)

    @orm.reconstructor
    def __init__(self):
        self.fields = ['spec','id', 'spec_value']


#spu-规格表
class Light_Spu_Spec(db.Model):
    __tablename__ = 'light_spu_spec'

    spu_id = db.Column(db.Integer , db.ForeignKey('light_spu.id'),primary_key=True)
    spec_id = db.Column(db.Integer , db.ForeignKey('light_spec.id'),primary_key=True)
    spu = db.relationship(Light_Spu , backref=db.backref("spu_specs",cascade="all, delete-orphan"))
    spec = db.relationship(Light_Spec , backref=db.backref("spec_spus"))
    spu_name = association_proxy('spu','name')
    spec_name = association_proxy('spec','spec_name')

    def __init__(self, selspec=None ,selspu=None):
        self.spec = selspec
        self.spu = selspu

#sku表

class Light_Sku(Base):
    __tablename__ = 'light_sku'
    id = Column(db.Integer , primary_key=True)
    sku_num = Column(db.String(50) , unique=True,nullable=False) #sku编号
    sku_name =  Column(db.String(50)) #规格商品名称
    price = Column(db.Float ,nullable=False)
    stock = Column(db.Integer,nullable=False,default=0)
    spu_id = db.Column(db.Integer , db.ForeignKey('light_spu.id'),nullable=False)
    spu = db.relationship(Light_Spu , backref=db.backref("spu_skus"))
    spec_values = association_proxy('sku_specs','spec_value')

    def __str__(self):
        return "{}".format(self.sku_name)

    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'sku_num','sku_name','price','stock','spec_values']
    # spec_value_names = association_proxy('sku_specs','spec_value_name')

#sku-spec对应表

class Light_sku_spec(Base):
    __tablename__ = 'light_sku_spec'
    id = Column(db.Integer , primary_key=True)
    sku_id = db.Column(db.Integer , db.ForeignKey('light_sku.id'))
    sku = db.relationship(Light_Sku , backref=db.backref("sku_specs",cascade="all, delete-orphan"))
    spec_value_id = db.Column(db.Integer , db.ForeignKey('light_spec_value.id'))
    spec_value = db.relationship(Light_Spec_Value , backref=db.backref("svalue_skus"))

    def __init__(self , selspec_value=None , selsku=None):
        self.spec_value = selspec_value
        self.sku = selsku

#
# #使用场景
# class Light_Sence(Base):
#     __tablename__ = 'light_sence'
#     id = Column(db.Integer , primary_key=True , autoincrement=True)
#     name = Column(db.String(50) , nullable=True)
#     code = Column(db.String(20),unique=True)
#     desc = Column(db.String(50), nullable=True)
#
#     def __str__(self):
#         return "{}".format(self.name)
#
# #风格
# class Light_Style(Base):
#     __tablename__ = 'light_style'
#     id = Column(db.Integer , primary_key=True , autoincrement=True)
#     name = Column(db.String(50) , nullable=True)
#     code = Column(db.String(20) , nullable=True)
#     desc = Column(db.String(50), nullable=True)
#
#     def __str__(self):
#         return "{}".format(self.name)


