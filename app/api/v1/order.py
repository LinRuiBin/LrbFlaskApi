from flask import request, jsonify

from app.libs.redprint import Redprint
from app.libs.error_code import ClientTypeError, Success,NodataReponse,SuccessReponse,FailReponse
from app.models.goods import *
from app.models.order import *
from app.models.base import *


api = Redprint('order')


@api.route('/', methods=['GET'])
def getOrders():

    orders = PayOrder.query.all()
    return SuccessReponse(msg='获取所有订单',data=orders)
