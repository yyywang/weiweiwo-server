# -*- coding: utf-8 -*-
"""
  Created by Wesley on 2020/1/3.
"""
from collections import namedtuple
from flask_httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer \
    as Serializer, BadSignature, SignatureExpired
from flask import current_app, g, request
from app.libs.error_code import AuthFailed, Forbidden
from app.libs.scope import is_in_scope

auth = HTTPBasicAuth()
User = namedtuple('User', ['uid', 'ac_type', 'is_admin'])


@auth.verify_password
def verify_password(token, password):
    user_info = verify_auth_token(token)
    if not user_info:
        return False
    else:
        g.user = user_info
        return True


def verify_auth_token(token):
    """
    解密Token
    若未抛出异常，则解密成功，校验通过
    若抛出BadSignature异常，则说明Token不合法
    :param token: 
    :return: 
    """
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token) # 解密Token
    except BadSignature:
        raise AuthFailed(msg='token is invalid',
                         error_code=1002)
    except SignatureExpired:
        raise AuthFailed(msg='token is expired',
                         error_code=1003)
    uid = data['uid']
    ac_type = data['type']
    scope = data['scope']
    allow = is_in_scope(scope, request.endpoint)
    if not allow:
        raise Forbidden()
    return User(uid, ac_type, scope)