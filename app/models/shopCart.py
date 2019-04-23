from sqlalchemy import inspect, Column, Integer, String, SmallInteger, orm
from app.libs.error_code import NotFound, AuthFailed
from app.models.base import Base, db, MixinJSONSerializer
from app.models.user import *
from app.models.goods import Light_Spu,Light_Sku

class ShopCart(Base):
    __tablename__ = 'shopcart'

    id = db.Column(db.Integer , primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship(User, backref=db.backref("shopCarts"))
    sku_id = db.Column(db.Integer, db.ForeignKey('light_sku.id'), nullable=False)
    sku = db.relationship(Light_Sku)
    quantity = db.Column(db.Integer, nullable=False)
