from sqlalchemy import inspect, Column, Integer, String, SmallInteger, orm
from app import app
from app.libs.error_code import NotFound, AuthFailed
from app.models.base import Base, db, MixinJSONSerializer
from app.models.user import *
from app.models.adress import *
from app.models.goods import *


class PayOrder(Base):
    __tablename__ = 'pay_order'
    __table_args__ = (
        db.Index('idx_user_id_status', 'user_id', 'order_status'),
    )

    id = db.Column(db.Integer, primary_key=True)
    order_sn = db.Column(db.String(40), nullable=False, unique=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship(User, backref=db.backref("orders"))

    total_price = db.Column(db.Float, nullable=False)
    yun_price = db.Column(db.Float,default=0)
    pay_price = db.Column(db.Float, nullable=False)
    pay_sn = db.Column(db.String(128))
    prepay_id = db.Column(db.String(128))
    note = db.Column(db.Text)
    order_status = db.Column(db.Integer, nullable=False)

    express_address_id = db.Column(db.Integer, db.ForeignKey('adress.id'), nullable=False)
    express_address = db.relationship(Adress)
    express_status = db.Column(db.Integer)
    express_info = db.Column(db.String(100))

    comment_status = db.Column(db.Integer)
    pay_time = db.Column(db.DateTime)
    # update_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    # create_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())

    @property
    def pay_status(self):
        tmp_status = self.order_status
        if self.order_status == 1:
            tmp_status = self.express_status
            if self.express_status == 1 and self.comment_status == 0:
                tmp_status = -5
            if self.express_status == 1 and self.comment_status == 1:
                tmp_status = 1
        return tmp_status

    @property
    def status_desc(self):
        return app.config['PAY_STATUS_DISPLAY_MAPPING'][ str( self.pay_status )]

    @property
    def order_number(self):
        order_number = self.create_time.strftime("%Y%m%d%H%M%S")
        order_number = order_number + str(self.id).zfill(5)
        return order_number

    def __str__(self):
        return "{}".format(self.order_sn)

    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'order_sn','note','order_status','pay_time','total_price','yun_price','pay_price',]


#订单商品
class OrderItem(Base):

    __tablename__ = 'pay_order_item'

    id = db.Column(db.Integer, primary_key=True)
    pay_order_id =  db.Column(db.Integer, db.ForeignKey('pay_order.id'), nullable=False)
    pay_order = db.relationship(PayOrder, backref=db.backref("orderItems"))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship(User, backref=db.backref("orderItems"))

    sku_id = db.Column(db.Integer, db.ForeignKey('light_sku.id'), nullable=False)
    sku = db.relationship(Light_Sku)
    quantity = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    price = db.Column(db.Float, nullable=False, server_default=db.FetchedValue())
    note = db.Column(db.Text)

    def __str__(self):
        return "{}*{}".format(self.sku.sku_name,self.quantity)

    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'sku', 'quantity','price','note']



class OauthAccessToken(Base):
    __tablename__ = 'oauth_access_token'

    id = db.Column(db.Integer, primary_key=True)
    access_token = db.Column(db.String(600), nullable=False)
    expired_time = db.Column(db.DateTime, nullable=False, index=True)