# -*- coding: utf-8 -*-
"""
  Created by Wesley on 2020/1/3.
"""
from flask import current_app
from app.libs.enums import ClientTypeEnum
from app.libs.error_code import AuthFailed, Success
from app.libs.redprint import Redprint
from app.models.user import User
from app.validators.auth import ClientForm, TokenForm
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature

api = Redprint('token')

@api.route('', methods=['POST'])
def get_token():
    form = ClientForm().validate_for_api()
    promise = {
        ClientTypeEnum.USER_EMAIL: User.verify,
        ClientTypeEnum.USER_MINA: User.verify_mina
    }
    identity = promise[ClientTypeEnum(form.type.data)](
        form.account.data,
        form.secret.data
    )
    # Token
    expiration = current_app.config['TOKEN_EXPIRATION']
    token = generate_auth_token(identity['uid'],
                                form.type.data,
                                identity['scope'],
                                expiration)
    # 用序列化器生成的Token不是普通的字符串
    # 需要调用decode转码
    t = {
        'token': token.decode('ascii')
    }
    return Success(data=t), 201


@api.route('/secret', methods=['POST'])
def get_token_info():
    """获取令牌信息"""
    form = TokenForm().validate_for_api()
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(form.token.data, return_header=True)
    except SignatureExpired:
        raise AuthFailed(msg='token is expired', error_code=1003)
    except BadSignature:
        raise AuthFailed(msg='token is invalid', error_code=1002)

    r = {
        'scope': data[0]['scope'],
        'create_at': data[1]['iat'],
        'expire_in': data[1]['exp'],
        'uid': data[0]['uid']
    }
    return Success(data=r)

def generate_auth_token(uid, ac_type, scope=None,
                        expiration=7200):
    """
    生成令牌
    :param uid: identity of user 
    :param ac_type: client type
    :param scope: auth scope
    :param expiration: expiration time
    :return: 
    """
    s = Serializer(current_app.config['SECRET_KEY'],
                   expires_in=expiration)
    # 调用序列化器的dumps方法将需要写入的信息以字典形式写入Token中
    # 返回值为字符串
    return s.dumps({
        'uid': uid,
        'type': ac_type.value,
        'scope': scope
    })