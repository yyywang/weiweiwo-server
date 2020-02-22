# -*- coding: utf-8 -*-
"""
  Created by Wesley on 2020/2/20.
"""
import time
from flask import current_app
from sqlalchemy import or_
from app.libs.error_code import ParameterException, Success
from app.libs.jsonify_helper import process_rsp_pagination
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.libs.wx import get_access_token, get_a_unlimit_code
from app.models.rescue import Rescue
from app.models.seek_help import SeekHelp
from app.validators.forms import SearchSHOrRescue
from app.validators.wx import AUnlimitCodeForm
from app.libs.extensions import cache

api = Redprint('common')


@api.route('/search')
@auth.login_required
def search_sh_or_rescue():
    """搜索 求喂养/我能帮 信息，支持 详细地址/手机号搜索"""
    form = SearchSHOrRescue().validate_for_api()
    q = '%' + form.q.data + '%'
    per_page = current_app.config['SEARCH_NUM_PER_PAGE']
    if form.category.data == 'seek-help':
        pagination = SeekHelp.query.filter(
            SeekHelp.status == 1,
            or_(SeekHelp.address.like(q), SeekHelp.phone.like(q))
        ).paginate(per_page=per_page, page=int(form.page.data))
    elif form.category.data == 'rescue':
        pagination = Rescue.query.filter(
            Rescue.status == 1,
            or_(Rescue.address.like(q), Rescue.phone.like(q))
        ).paginate(per_page=per_page, page=int(form.page.data))
    else:
        raise ParameterException()

    return Success(data=process_rsp_pagination(pagination))


@api.route('/wx/unlimit-code', methods=['POST'])
@auth.login_required
def get_a_wx_unlimit_code():
    """获取一张无限制的微信小程序二维码
    wx_doc: https://developers.weixin.qq.com/miniprogram/dev/api-backend/open-api/qr-code/wxacode.getUnlimited.html
    """
    form = AUnlimitCodeForm().validate_for_api()
    data = dict(img_url=get_a_unlimit_code(form.data))
    return Success(data=data)


@api.route('/test')
@auth.login_required
@cache.cached()
def test():
    time.sleep(1)
    wx_access_key = get_access_token()
    return Success(data=wx_access_key)