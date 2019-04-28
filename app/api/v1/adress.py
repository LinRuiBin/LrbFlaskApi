from flask import request, jsonify

from app.libs.redprint import Redprint
from app.libs.error_code import ClientTypeError, Success,NodataReponse,SuccessReponse,FailReponse
from app.models.goods import *
from app.models.order import *
from app.models.base import *
from app.models.shopCart import *
from app.models.adress import *

api = Redprint('adress')


@api.route('/', methods=['GET'])
def getAllAdress():

    adress = Adress.query.all()
    return SuccessReponse(msg='获取地址',data=adress)