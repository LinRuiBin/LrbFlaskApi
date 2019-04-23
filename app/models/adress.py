from sqlalchemy import inspect, Column, Integer, String, SmallInteger, orm
from app.libs.error_code import NotFound, AuthFailed
from app.models.base import Base, db, MixinJSONSerializer
from app.models.user import *
from sqlalchemy.ext.associationproxy import association_proxy
from datetime import datetime


#收货地址
class Adress(Base):
    __tablename__ = 'adress'

    id = db.Column(db.Integer , primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship(User, backref=db.backref("adresses"))

    nickname = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())
    mobile = db.Column(db.String(11), nullable=False, server_default=db.FetchedValue())
    province_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    province_str = db.Column(db.String(50), nullable=False, server_default=db.FetchedValue())
    city_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    city_str = db.Column(db.String(50), nullable=False, server_default=db.FetchedValue())
    area_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    area_str = db.Column(db.String(50), nullable=False, server_default=db.FetchedValue())
    address = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    is_default = db.Column(db.Integer, nullable=False,default=0)


    def __str__(self):
        return "{}{}{}{}".format(self.province_str,self.city_str,self.area_str,self.address)