# -*- coding: utf-8 -*-
import hashlib,time,random,decimal,json
from app.models.goods import *
from app.models.order import *
from app.models.adress import Adress
from app.models.base import *
from app.libs.error_code import FailReponse
from app.libs.helper import getCurrentDate

"""
创建订单
params = {
        "note":note,
        'address_id':address_info.id,
        'info':{
            'mobile':address_info.mobile,
            'nickname':address_info.nickname,
            "address":"%s%s%s%s"%( address_info.province_str,address_info.city_str,address_info.area_str,address_info.address )
        }
    }
    
items  [{'sku_id':1,'count':2,'price':10.00}]
uid userId
"""
class PayService():

    def __init__(self):
        pass

    def createOrder(self,uid,items = None,params = None):
        resp = {'status': 1, 'msg': '操作成功~', 'data': {}}
        user = User.query.filter_by(id=uid).first_or_404()
        pay_price  = decimal.Decimal( 0.00 )
        continue_cnt = 0
        goods_ids = []
        for item in items:
            if decimal.Decimal( item['price'] ) < 0 :
                continue_cnt += 1
                continue

            pay_price = pay_price +  decimal.Decimal( item['price'] ) * int( item['count'] )
            goods_ids.append( item['sku_id'] )

        if continue_cnt >= len(items ) :
            resp['status'] = -1
            resp['msg'] = '商品items为空~~'
            return resp

        yun_price = params['yun_price'] if params and 'yun_price' in params else 0
        note = params['note'] if params and 'note' in params else ''
        address_id = params['address_id'] if params and 'address_id' in params else 0
        info = params['info'] if params and 'info' in params else {}
        yun_price = decimal.Decimal( yun_price )
        total_price = pay_price + yun_price
        try:
            #为了防止并发库存出问题了，selectfor update
            tmp_good_list = db.session.query( Light_Sku ).filter( Light_Sku.id.in_( goods_ids ) )\
                .with_for_update().all()

            tmp_good_stock_mapping = {}
            for tmp_item in tmp_good_list:
                tmp_good_stock_mapping[ tmp_item.id ] = tmp_item.stock

            model_pay_order = PayOrder()
            model_pay_order.order_sn = self.geneOrderSn()
            model_pay_order.user = user
            model_pay_order.total_price = total_price
            model_pay_order.yun_price = yun_price
            model_pay_order.pay_price = pay_price
            model_pay_order.note = note
            model_pay_order.order_status = -8
            model_pay_order.express_status = -8
            model_pay_order.express_address_id = address_id
            #model_pay_order.express_info = json.dumps(  info  )
            # model_pay_order.updated_time = model_pay_order.created_time = getCurrentDate()
            db.session.add( model_pay_order )
            #db.session.flush()
            for item in items:
                tmp_left_stock =  tmp_good_stock_mapping[ item['sku_id'] ]

                if decimal.Decimal(item['price']) < 0:
                    continue

                if int( item['count'] ) > int( tmp_left_stock ):
                    raise FailReponse(msg='库存不足')
                    # raise Exception( "您购买的这美食太火爆了，剩余：%s,你购买%s~~"%( tmp_left_stock,item['number'] ) )

                tmp_ret = Light_Sku.query.filter_by( id = item['sku_id'] ).update({
                    "stock":int(tmp_left_stock) - int(item['count'])
                })
                if not tmp_ret:
                    raise FailReponse(msg='下单失败请重新下单')
                    # raise Exception("下单失败请重新下单")

                tmp_pay_item = OrderItem()
                tmp_pay_item.pay_order = model_pay_order
                tmp_pay_item.user = user
                tmp_pay_item.quantity = item['count']
                tmp_pay_item.price = item['price']
                tmp_pay_item.sku_id = item['sku_id']
                tmp_pay_item.note = note
                # tmp_pay_item.updated_time = tmp_pay_item.created_time = getCurrentDate()
                db.session.add( tmp_pay_item )
                #db.session.flush()

                # FoodService.setStockChangeLog( item['id'],-item['number'],"在线购买" )
            db.session.commit()
            resp['data'] = {
                'id' : model_pay_order.id,
                'order_sn' : model_pay_order.order_sn,
                'total_price':str( total_price )
            }
        except Exception as e:
            if isinstance(e, FailReponse):
                raise e
            db.session.rollback()
            raise FailReponse(msg='下单失败请重新下单')
        return resp

    def closeOrder(self, pay_order_id=0):
        if pay_order_id < 1:
            return False
        pay_order_info = PayOrder.query.filter_by(id=pay_order_id, status=-8).first()
        if not pay_order_info:
            return False

        pay_order_items = OrderItem.query.filter_by(pay_order_id=pay_order_id).all()
        if pay_order_items:
            # 需要归还库存
            for item in pay_order_items:
                tmp_food_info = Light_Sku.query.filter_by(id=item.sku_id).first()
                if tmp_food_info:
                    tmp_food_info.stock = tmp_food_info.stock + item.quantity
                    # tmp_food_info.updated_time = getCurrentDate()
                    db.session.add(tmp_food_info)
                    db.session.commit()


        pay_order_info.status = 0
        # pay_order_info.updated_time = getCurrentDate()
        db.session.add(pay_order_info)
        db.session.commit()
        return True

    def orderSuccess(self, pay_order_id=0, params=None):
        try:
            pay_order_info = PayOrder.query.filter_by(id=pay_order_id).first()
            if not pay_order_info or pay_order_info.order_status not in [-8, -7]:
                return True

            pay_order_info.pay_sn = params['pay_sn'] if params and 'pay_sn' in params else ''
            pay_order_info.order_status = 1
            pay_order_info.express_status = -7
            # pay_order_info.updated_time = getCurrentDate()
            db.session.add(pay_order_info)

            #记录库存变化
            # pay_order_items = OrderItem.query.filter_by(pay_order_id=pay_order_id).all()
            # for order_item in pay_order_items:
            #     tmp_model_sale_log = FoodSaleChangeLog()
            #     tmp_model_sale_log.food_id = order_item.food_id
            #     tmp_model_sale_log.quantity = order_item.quantity
            #     tmp_model_sale_log.price = order_item.price
            #     tmp_model_sale_log.member_id = order_item.member_id
            #     tmp_model_sale_log.created_time = getCurrentDate()
            #     db.session.add(tmp_model_sale_log)

            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(e)
            return False

        # 加入通知队列，做消息提醒和
        # QueueService.addQueue("pay", {
        #     "member_id": pay_order_info.member_id,
        #     "pay_order_id": pay_order_info.id
        # })
        return True

    def addPayCallbackData(self, pay_order_id=0, type='pay', data=''):
        #记录回调信息
        # model_callback = PayOrderCallbackData()
        # model_callback.pay_order_id = pay_order_id
        # if type == "pay":
        #     model_callback.pay_data = data
        #     model_callback.refund_data = ''
        # else:
        #     model_callback.refund_data = data
        #     model_callback.pay_data = ''
        #
        # model_callback.created_time = model_callback.updated_time = getCurrentDate()
        # db.session.add(model_callback)
        # db.session.commit()
        return True


    def geneOrderSn(self):
        m = hashlib.md5()
        sn = None
        while True:
            str = "%s-%s"%( int( round( time.time() * 1000) ),random.randint( 0,9999999 ) )
            m.update(str.encode("utf-8"))
            sn = m.hexdigest()
            if not PayOrder.query.filter_by( order_sn = sn  ).first():
                break
        return sn
