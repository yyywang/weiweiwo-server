# -*- coding: utf-8 -*-
"""
  Created by Wesley on 2020/1/10.
"""
import requests
from flask import current_app
from app.libs.error_code import ServerError, ClientTypeError


def wx_get_user_by_code(code):
    """从微信服务器获取openid"""
    base_url = current_app.config['WX_LOGIN_BASE_URL']
    params = {
        "appid": current_app.config['APP_ID'],
        "secret": current_app.config['APP_SECRET'],
        "js_code": code,
        "grant_type": "authorization_code"
    }

    try:
        wx_data = requests.get(base_url, params=params).json()
    except Exception:
        raise ServerError()

    if wx_data.get('openid', None):
        # 请求成功
        return wx_data
    elif wx_data.get('errcode', None):
        # code 出错
        raise ClientTypeError(msg=wx_data.get('errmsg', None))
    else:
        raise ServerError()