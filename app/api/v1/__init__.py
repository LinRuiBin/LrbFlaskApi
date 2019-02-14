"""
 Created by LRB on 2018/5/8.
"""
from flask import Blueprint
from app.api.v1 import user, book, client, token,gift

__author__ = 'LRB'

docApis_v1= ['v1.user','v1.book','v1.client','v1.token','v1.gift']

def create_blueprint_v1():
    bp_v1 = Blueprint('v1', __name__)

    user.api.register(bp_v1)
    book.api.register(bp_v1)
    client.api.register(bp_v1)
    token.api.register(bp_v1)
    gift.api.register(bp_v1)
    return bp_v1
