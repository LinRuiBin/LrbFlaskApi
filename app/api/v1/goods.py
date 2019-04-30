from flask import request, jsonify

from app.libs.redprint import Redprint
from app.libs.error_code import ClientTypeError, Success,NodataReponse,SuccessReponse,FailReponse
from app.models.goods import *
from app.models.base import *

api = Redprint('goods')

#获取分类下的所有叶子节点
def getAllLeafCatForCat(cat):

    result = []
    if cat.is_leaf == True:
        result.append(cat)
        return result

    subCats = cat.sub_cats
    if not subCats:
        return []
    for subCat in subCats:
        result.extend(getAllLeafCatForCat(subCat))
    return result


"""

获取sku

cat_id:分类id 传入获取分类下的sku
spu_id:获取spu下的sku

page:页数
q:搜索

"""
@api.route('/', methods=['GET'])
def getIndexGoods():

    data = {}
    req = request.values
    cat_id = int(req['cat_id']) if 'cat_id' in req else 0
    spu_id = int(req['spu_id']) if 'spu_id' in req else 0
    page = int(req['page']) if 'page' in req else 1
    if page < 1:
        page = 1

    page_size = 10
    offset = (page - 1) * page_size

    leaf_cats = [] #找出此分类id的所有叶子分类

    if cat_id>0 and spu_id>0:
        return FailReponse(msg='参数错误')

    if cat_id > 0:
       cat = Light_Category.query.filter_by(id=cat_id).all()
       if cat:
           cat = cat[0]
           if cat.is_leaf == True:
               leaf_cats.append(cat)
           else:
               leaf_cats = getAllLeafCatForCat(cat)
       else:
           return NodataReponse(msg='没有此分类')


    spu_query = Light_Spu.query
    if leaf_cats:
        cat_ids = []
        for cat in leaf_cats:
            cat_ids.append(cat.id)

        spu_query.filter(Light_Spu.category_id.in_(cat_ids))

    if cat_id > 0:
      spu_list = spu_query.order_by(Light_Spu.id.desc()).offset(offset).limit(page_size).all()
      for spu in spu_list:
          spu.update_fields('id','name','desc')

      data["spus"] = spu_list
      data['page'] = page


    if spu_id>0:
        spu = spu_query.filter(Light_Spu.id==spu_id).first()
        data['spu'] = spu

    return SuccessReponse(msg='获取成功',data=data)



