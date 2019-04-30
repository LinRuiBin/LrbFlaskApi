from flask import request, jsonify,g
from app.libs.token_auth import auth
import json, decimal

from app.libs.redprint import Redprint
from app.libs.error_code import ClientTypeError, Success,NodataReponse,SuccessReponse,FailReponse
from app.models.goods import *
from app.models.order import *
from app.models.adress import Adress
from app.models.base import *


api = Redprint('order')

@api.route('/', methods=['GET'])
@auth.login_required
def getOrders():
    orders = PayOrder.query.all()
    return SuccessReponse(msg='获取所有订单',data=orders)


@api.route('/info', methods=['POST'])
@auth.login_required
def orderInfo():
    req = request.values
    data = {}
    params_goods = req['goods'] if 'goods' in req else None
    uid = g.user.uid
    user = User.query.filter_by(id=uid).first_or_404()
    params_goods_list = []
    # [{'sku_id':1,'count':2}]
    if params_goods:
        params_goods_list = json.loads(params_goods)

    good_dic = {}
    for item in params_goods_list:
        good_dic[item['sku_id']] = item['count']
    good_ids = good_dic.keys()
    good_list = Light_Sku.query.filter(Light_Sku.id.in_(good_ids)).all()
    yun_price = pay_price = float(0.00)

    for sku in good_list:
        pay_price = pay_price + sku.price * int(good_dic[sku.id])
        sku.append('count')
        sku.count = int(good_dic[sku.id])
        sku.hide('spec_values')


    data['skus'] = good_list
    data['pay_price'] = pay_price

    adress = Adress.query.filter_by(is_default = 1,user_id = user.id).first()
    if adress:
        adress.update_fields('id','mobile','nickname','total_adress',)
        adress.total_adress = "{}{}{}{}".format(adress.province_str,adress.city_str,adress.area_str,adress.address)

    data['default_adress'] = adress

    return SuccessReponse(msg='获取成功',data=data)


