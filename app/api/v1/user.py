# -*- coding: utf-8 -*-
"""
  Created by Wesley on 2019/12/30.
"""
from flask import jsonify, g, current_app
from app.libs.error_code import DeleteSuccess, Success
from app.libs.jsonify_helper import process_rsp_pagination
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.base import db
from app.models.seek_help import SeekHelp
from app.models.user import User
from app.validators.auth import UserUpdateForm, UserSeekHelpListFrom

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


@api.route('/profile', methods=['PUT'])
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


@api.route('/seek-help')
@auth.login_required
def get_seek_help_list():
    """获取我的求喂养列表，分页返回"""
    form = UserSeekHelpListFrom().validate_for_api()
    user = User.query.filter_by(id=g.user.uid).first_or_404()
    per_page = current_app.config['SEEK_HELP_PER_PAGE']
    pagination = SeekHelp.query.filter_by().with_parent(user).paginate(
        page=int(form.page.data), per_page=per_page)
    return Success(data=process_rsp_pagination(pagination))


@api.route('/seek-help/<int:sid>')
@auth.login_required
def get_seek_help(sid):
    """获取用户发布的 id=sid 求喂养数据"""
    user = User.query.filter_by(id=g.user.uid).first_or_404()
    obj_seek_help = SeekHelp.query.filter_by(id=sid,author_id=user.id).first_or_404()
    return Success(data=obj_seek_help)


@api.route('/seek-help/<int:sid>/cancel-or-not', methods=['PUT'])
@auth.login_required
def cancel_or_not_seek_help(sid):
    """取消/恢复 id=sid 的求喂养信息展示"""
    user = User.query.filter_by(id=g.user.uid).first_or_404()
    user.cancel_or_not(sid)
    return Success()