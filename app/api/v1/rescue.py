# -*- coding: utf-8 -*-
"""
  Created by Wesley on 2020/2/7.
"""
from flask import current_app, jsonify, g
from werkzeug.exceptions import HTTPException
from app.libs.map import get_address_by_location_from_tx_map
from app.libs.token_auth import auth
from app.libs.error_code import Success, ParameterException
from app.libs.jsonify_helper import process_rsp_pagination
from app.libs.redprint import Redprint
from app.models.base import db
from app.models.rescue import Rescue
from app.models.seek_help import SeekHelp
from app.validators.forms import RescueForm, GetDataByLocationForm

api = Redprint('rescue')


@api.route('', methods=['POST'])
@auth.login_required
def create_rescue():
    """创建我能帮（Rescue）"""
    form = RescueForm().validate_for_api()
    # 通过经纬度从腾讯地图获得位置描述：省/市/区
    location = get_address_by_location_from_tx_map(form.latitude.data, form.longitude.data)
    with db.auto_commit():
        obj_rescue = Rescue()
        obj_rescue.set_attrs(form.data)
        obj_rescue.set_attrs(location['result']['address_component'])
        obj_rescue.author_id = g.user.uid
        db.session.add(obj_rescue)
    return Success(data={"id": obj_rescue.id})


@api.route('/location')
@auth.login_required
def get_rescues_by_location():
    """获取 我能帮 数据列表，根据 省/市/区 筛选
    按发布时间倒序排列

    params: 
        *<int:page> 第几页
        *<str:province> 省
        *<str:city> 市
        *<str:district> 区
    """
    form = GetDataByLocationForm().validate_for_api()
    per_page = current_app.config['RESCUE_LIST_PER_PAGE']
    try:
        if form.province.data == "全部":
            all_rescue = Rescue.query.filter_by(cancel=False).order_by(
                Rescue.create_time.desc()).paginate(page=int(form.page.data), per_page=per_page)
        elif form.city.data == "全部":
            all_rescue = Rescue.query.filter_by(cancel=False,province=form.province.data).order_by(
                Rescue.create_time.desc()).paginate(page=int(form.page.data), per_page=per_page)
        elif form.district.data == "全部":
            all_rescue = Rescue.query.filter_by(cancel=False,province=form.province.data, city=form.city.data).order_by(
                Rescue.create_time.desc()).paginate(page=int(form.page.data), per_page=per_page)
        else:
            # 按 省/市/区 筛选
            all_rescue = Rescue.query.filter_by(
                cancel=False, province=form.province.data, city=form.city.data, district=form.district.data).order_by(
                Rescue.create_time.desc()).paginate(page=int(form.page.data), per_page=per_page)
    except HTTPException:
        raise ParameterException(msg='page out range')

    return Success(data=process_rsp_pagination(all_rescue))


@api.route('/<int:sid>')
def get_seek_help(sid):
    """返回 id=sid 的 SeekHelp"""
    obj_seek_help = SeekHelp.query.filter_by(id=sid).first_or_404()
    return jsonify(obj_seek_help)