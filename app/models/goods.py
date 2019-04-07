from sqlalchemy import inspect, Column, Integer, String, SmallInteger, orm
from app.libs.error_code import NotFound, AuthFailed
from app.models.base import Base, db, MixinJSONSerializer
from sqlalchemy.ext.associationproxy import association_proxy
import datetime


#多对一 照明分类
class Light_Category(Base):
    __tablename__ = 'light_category'
    id = Column(db.Integer , primary_key=True , autoincrement=True)
    name = Column(db.String(50) , nullable=False)
    code = Column(db.String(20),unique=True)  #分类编码
    desc = Column(db.String(50), nullable=True)

    def __str__(self):
        return "{}".format(self.name)

#灯其他分类  多对多
class Light_other_Category(Base):
    __tablename__ = 'light_other_category'
    id = Column(db.Integer , primary_key=True)
    name = Column(db.String(50) , nullable=False)
    code = Column(db.String(20),unique=True)  #分类编码
    desc = Column(db.String(50), nullable=True)

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
    name = Column(db.String(50) , nullable=False)
    spu_num = Column(db.String(50) , unique=True,nullable=False)  # 商品编码
    desc = Column(db.String(50) , nullable=True)
    category_id = Column(db.Integer,db.ForeignKey('light_category.id'))
    category = db.relationship(Light_Category , backref='lights')
    other_categories = association_proxy("spu_other_categorys",'other_category')
    # def __str__(self):
    #     return "{}".format(self.name)





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


