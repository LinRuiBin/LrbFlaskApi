from sqlalchemy import inspect, Column, Integer, String, SmallInteger, orm
from app.libs.error_code import NotFound, AuthFailed
from app.models.base import Base, db, MixinJSONSerializer
from app.models.user import *
from sqlalchemy.ext.associationproxy import association_proxy
from datetime import datetime


#收货地址
class Adress(Base):
    __tablename__ = 'adress'
    __table_args__ = (
        db.Index('idx_user_id_status', 'user_id', 'status'),
    )

    id = db.Column(db.Integer , primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship(User, backref=db.backref("adresses"))

    nickname = db.Column(db.String(20), nullable=False)
    mobile = db.Column(db.String(11), nullable=False)
    province_id = db.Column(db.Integer, nullable=False)
    province_str = db.Column(db.String(50), nullable=False)
    city_id = db.Column(db.Integer, nullable=False)
    city_str = db.Column(db.String(50), nullable=False)
    area_id = db.Column(db.Integer, nullable=False)
    area_str = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    addr_status = db.Column(db.Integer, nullable=False)
    is_default = db.Column(db.Integer, nullable=False,default=0)


    def __str__(self):
        return "{}{}{}{}".format(self.province_str,self.city_str,self.area_str,self.address)