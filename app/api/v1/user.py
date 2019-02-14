"""
 Created by LRB on 2018/5/7.

"""
from flask import jsonify, g

from app.libs.error_code import DeleteSuccess, AuthFailed
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.base import db
from app.models.user import User

__author__ = 'LRB'

api = Redprint('user')


@api.route('/<int:uid>', methods=['GET'])
@auth.login_required
def super_get_user(uid):
    """
    管理源获取指定用户信息
    :param uid:
    :return:
    """
    user = User.query.filter_by(id=uid).first_or_404()
    return jsonify(user)


@api.route('', methods=['GET'])
@auth.login_required
def get_user():
    """
    获取当前用户信息
    :return:
    """
    uid = g.user.id
    user = User.query.filter_by(id=uid).first_or_404()
    return jsonify(user)


@api.route('/<int:uid>', methods=['DELETE'])
def super_delete_user(uid):
    """
    管理员删除指定uid用户
    :param uid:
    :return:
    """
    pass


@api.route('', methods=['DELETE'])
@auth.login_required
def delete_user():
    """
    删除当前用户
    :return:
    """
    uid = g.user.uid
    with db.auto_commit():
        user = User.query.filter_by(id=uid).first_or_404()
        user.delete()
    return DeleteSuccess()


@api.route('', methods=['PUT'])
def update_user():
    """
    更新个人信息
    :return:
    """
    return 'update qiyue'


