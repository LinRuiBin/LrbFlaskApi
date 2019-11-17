
from sqlalchemy import inspect, Column, Integer, String, SmallInteger, orm
from app.libs.error_code import NotFound, AuthFailed
from app.models.base import Base, db, MixinJSONSerializer
from sqlalchemy.ext.associationproxy import association_proxy
from datetime import datetime



class User_Order_Info(Base):
    __tablename__ = 'user_order_info'
    id = Column(db.Integer , primary_key=True, autoincrement=True,default=1)#id
    study_Id = Column(db.String(100) , unique=True,nullable=False, primary_key=True) #学号
    name =  Column(db.String(100),nullable=False) #规格名称
    money = Column(db.Float ,nullable=False) #钱
    desc = Column(db.String(100)) #描述
    order_num = Column(db.String(100),nullable=False) #订单号

    def __str__(self):
        return "{}".format(self.name)