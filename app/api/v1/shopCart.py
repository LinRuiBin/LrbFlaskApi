from flask import request, jsonify

from app.libs.redprint import Redprint
from app.libs.error_code import ClientTypeError, Success,NodataReponse,SuccessReponse,FailReponse
from app.models.goods import *
from app.models.order import *
from app.models.base import *
from app.models.shopCart import *

api = Redprint('shopCart')


@api.route('/', methods=['GET'])
def getShopCarts():

    shopCarts = ShopCart.query.all()
    return SuccessReponse(msg='获取购物车',data=shopCarts)