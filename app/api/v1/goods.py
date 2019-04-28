from flask import request, jsonify

from app.libs.redprint import Redprint
from app.libs.error_code import ClientTypeError, Success,NodataReponse,SuccessReponse,FailReponse
from app.models.goods import *
from app.models.base import *

api = Redprint('goods')


@api.route('/', methods=['GET'])
def getIndexGoods():

    spus = Light_Spu.query.all()
    return SuccessReponse(msg='获取首页商品成功',data=spus)



