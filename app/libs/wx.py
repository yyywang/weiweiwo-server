# -*- coding: utf-8 -*-
"""
  Created by Wesley on 2020/1/10.
  关于微信服务端的函数
"""
import json
from datetime import datetime
import requests
from flask import current_app
from app.libs.error_code import ServerError, ClientTypeError
from app.libs.staging import set_value_by_key, get_value_by_key
from app.libs.util import dict_rm_none


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

def get_a_unlimit_code(data):
    """取一张无限制的微信小程序二维码"""
    base_url = current_app.config['GET_WX_A_UNLIMIT_CODE_BASE_URL']
    access_token = get_access_token()
    url = base_url + "?access_token=" + access_token
    data = dict_rm_none(data) # 剔除值为 None 的数据

    try:
        wx_data = requests.post(url, data=json.dumps(data))
        return wx_data.content
    except Exception:
        ServerError()


def send_subscribe_msg(touser=None, template_id=None, data=None,
                       page=None, miniprogram_state=None, lang=None):
    """
    发送订阅消息
    wx_doc: https://developers.weixin.qq.com/miniprogram/dev/api-backend/
            open-api/subscribe-message/subscribeMessage.send.html
    :param touser: 接收者（用户）的 openid
    :param template_id: 所需下发的订阅模板id
    :param data: 模板内容
    :param page: 点击模板卡片后的跳转页面
    :param miniprogram_state: 跳转小程序类型
    :param lang: 进入小程序查看”的语言类型
    :return: 
    """
    if touser is None or template_id is None or data is None:
        # 这3个参数必填
        raise ValueError()

    rq_data = dict(
        touser=touser,
        template_id=template_id,
        data=data,
        page=page,
        miniprogram_state=miniprogram_state,
        lang=lang
    )
    rq_data = dict_rm_none(rq_data)
    base_url = current_app.config['SEND_SUBSCRIBE_MSG_BASE_URL']
    url = base_url + "?access_token=" + get_access_token()
    requests.post(url, data=rq_data)


def get_access_token():
    """返回微信小程序 access_token"""
    access_token = get_access_token_from_staging()
    if access_token is None:
        access_token = get_access_token_from_wx()
    return access_token


def get_access_token_from_staging():
    """从数据库暂存区获取 access_token
    若数据库中 access_token 已过期返回 None"""
    return get_value_by_key('wx_access_token')

def get_access_token_from_wx():
    """从微信服务器获取 access_token """
    params = {
        "grant_type": "client_credential",
        "appid": current_app.config['APP_ID'],
        "secret": current_app.config['APP_SECRET']
    }
    base_url = current_app.config['GET_TOKEN_BASE_URL']

    index = 1
    while True:
        # 防止死循环
        index += 1
        if index > 5:
            raise ServerError(msg='get wx access_token timeout')
        try:
            response = requests.post(base_url, params).json()
            access_token = response.get('access_token')
            if access_token:
                # 将 token 存入暂存数据表
                expires_at = int(response.get('expires_in')) + int(datetime.now().timestamp())
                set_value_by_key(
                    key='wx_access_token',
                    value=access_token,
                    expires_at=expires_at,
                    des='微信小程序 access_token')
                return access_token
            elif response.get('errcode') == -1:
                # -1 代表微信服务器繁忙
                pass
            else:
                raise ServerError()
        except Exception:
            raise ServerError()