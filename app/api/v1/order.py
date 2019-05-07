from flask import request, jsonify,g
from app.libs.token_auth import auth
import json, decimal

from app.libs.redprint import Redprint
from app.libs.error_code import ClientTypeError, Success,NodataReponse,SuccessReponse,FailReponse
from app.models.goods import *
from app.models.order import *
from app.models.adress import Adress
from app.models.base import *
from app.service.PayService import *
from app.service.WeChatService import *
from app import app

api = Redprint('order')

@api.route('/', methods=['GET'])
@auth.login_required
def getOrders():
    orders = PayOrder.query.all()
    return SuccessReponse(msg='获取所有订单',data=orders)


"""
生成预览订单
goods:[{'sku_id':1,'count':2}  json 字符串 
返回地址 价格
"""
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



"""
创建订单
type  'cart' 购物车 else 直接购买
note 备注
adressid 地址
goods  json  [{'sku_id':1,'count':2,'price':10.00}] 商品

"""
@api.route("/create", methods=[ "POST"])
@auth.login_required
def orderCreate():

    req = request.values
    type = req['type'] if 'type' in req else ''
    note = req['note'] if 'note' in req else ''
    address_id = int( req['adressid'] ) if 'adressid' in req and req['adressid'] else 0
    params_goods = req['goods'] if 'goods' in req else None
    uid = g.user.uid
    user = User.query.filter_by(id=uid).first_or_404()

    items = []
    if params_goods:
        items = json.loads(params_goods)

    if len( items ) < 1:
        return FailReponse(msg='下单失败，并未选择商品')

    address_info = Adress.query.filter_by( id = address_id ).first()
    if not address_info:
         return FailReponse(msg='下单失败，快递地址不正确')

    target = PayService()
    params = {
        "note":note,
        'address_id':address_info.id,
        'info':{
            'mobile':address_info.mobile,
            'nickname':address_info.nickname,
            "address":"%s%s%s%s"%( address_info.province_str,address_info.city_str,address_info.area_str,address_info.address )
        }
    }
    resp = target.createOrder( uid ,items ,params)
    #如果是来源购物车的，下单成功将下单的商品去掉
    if resp['status'] == 1 and type == "cart":
        pass
        #CartService.deleteItem( member_info.id,items )

    return jsonify(resp)


"""
生成预支付单号 小程序
order_sn 订单号
"""
@api.route("/pay", methods=[ "POST"])
@auth.login_required
def orderPay():
    data = {}
    uid = g.user.uid
    user = User.query.filter_by(id=uid).first_or_404()
    req = request.values
    order_sn = req['order_sn'] if 'order_sn' in req else ''
    pay_order_info = PayOrder.query.filter_by( order_sn = order_sn,user_id = uid ).first()
    if not pay_order_info:
        return FailReponse(msg='系统繁忙。请稍后再试~~')

    oauth_bind_info = OauthMemberBind.query.filter_by( user_id =  uid ).first()
    if not oauth_bind_info:
        return FailReponse(msg='系统繁忙。请稍后再试~~')

    config_mina = app.config['MINA_APP']
    notify_url = app.config['APP']['domain'] + config_mina['callback_url']

    target_wechat = WeChatService( merchant_key=config_mina['paykey'] )

    data = {
        'appid': config_mina['appid'],
        'mch_id': config_mina['mch_id'],
        'nonce_str': target_wechat.get_nonce_str(),
        'body': '订餐',  # 商品描述
        'out_trade_no': pay_order_info.order_sn,  # 商户订单号
        'total_fee': int( pay_order_info.total_price * 100 ),
        'notify_url': notify_url,
        'trade_type': "JSAPI",
        'openid': oauth_bind_info.openid
    }

    pay_info = target_wechat.get_pay_info( pay_data=data)

    #保存prepay_id为了后面发模板消息
    pay_order_info.prepay_id = pay_info['prepay_id']
    db.session.add( pay_order_info )
    db.session.commit()

    data['pay_info'] = pay_info
    return SuccessReponse(msg='操作成功',data=data)


"""
支付成功微信回调
"""
@api.route("/callback", methods=[ "POST"])
def orderCallback():
    result_data = {
        'return_code': 'SUCCESS',
        'return_msg': 'OK'
    }
    header = {'Content-Type': 'application/xml'}
    config_mina = app.config['MINA_APP']
    target_wechat = WeChatService(merchant_key=config_mina['paykey'])
    callback_data = target_wechat.xml_to_dict( request.data )
    app.logger.info( callback_data  )
    sign = callback_data['sign']
    callback_data.pop( 'sign' )
    gene_sign = target_wechat.create_sign( callback_data )
    app.logger.info(gene_sign)
    if sign != gene_sign:
        result_data['return_code'] = result_data['return_msg'] = 'FAIL'
        return target_wechat.dict_to_xml(result_data), header
    if callback_data['result_code'] != 'SUCCESS':
        result_data['return_code'] = result_data['return_msg'] = 'FAIL'
        return target_wechat.dict_to_xml(result_data), header

    order_sn = callback_data['out_trade_no']
    pay_order_info = PayOrder.query.filter_by(order_sn=order_sn).first()
    if not pay_order_info:
        result_data['return_code'] = result_data['return_msg'] = 'FAIL'
        return target_wechat.dict_to_xml(result_data), header

    if int( pay_order_info.total_price * 100  ) != int( callback_data['total_fee'] ):
        result_data['return_code'] = result_data['return_msg'] = 'FAIL'
        return target_wechat.dict_to_xml(result_data), header

    if pay_order_info.status == 1:
        return target_wechat.dict_to_xml(result_data), header

    target_pay = PayService()
    target_pay.orderSuccess( pay_order_id = pay_order_info.id,params = { "pay_sn":callback_data['transaction_id'] } )
    target_pay.addPayCallbackData( pay_order_id = pay_order_info.id, data = request.data)
    return target_wechat.dict_to_xml(result_data), header
