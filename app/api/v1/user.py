# -*- coding: utf-8 -*-
"""
  Created by Wesley on 2019/12/30.
"""
from flask import jsonify, g
from app.libs.error_code import DeleteSuccess, Success
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.base import db
from app.models.user import User
from app.validators.auth import UserUpdateForm

api = Redprint('user')


@api.route('/<int:uid>', methods=['GET'])
@auth.login_required
def super_get_user(uid):
    user = User.query.filter_by(id=uid) \
        .first_or_404(description='user not found')
    return jsonify(user)


@api.route('', methods=['GET'])
@auth.login_required
def get_user():
    uid = g.user.uid
    user = User.query.filter_by(id=uid)\
        .first_or_404(description='user not found')
    return jsonify(user)


@api.route('', methods=['PUT'])
@auth.login_required
def update_user():
    """更新用户信息"""
    form = UserUpdateForm().validate_for_api()
    user = User.query.filter_by().first_or_404()
    with db.auto_commit():
        user.set_attrs(form.data)
    return Success()


@api.route('', methods=['DELETE'])
@auth.login_required
def delete_user():
    uid = g.user.uid
    with db.auto_commit():
        user = User.query.filter_by(id=uid).first_or_404()
        user.delete()
    return DeleteSuccess()