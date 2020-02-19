# -*- coding: utf-8 -*-
"""
  Created by Wesley on 2019/12/31.
"""
from app.libs.enums import ClientTypeEnum
from app.libs.error_code import Success
from app.libs.redprint import Redprint
from app.libs.wx import wx_get_user_by_code
from app.models.user import User
from app.validators.auth import ClientForm, UserEmailForm

api = Redprint("client")

@api.route('/register', methods=['POST'])
def create_client():
    # 如果校验不通过会抛出异常，后面的代码就不执行了
    form = ClientForm().validate_for_api()
    # 根据不同的客户端执行不同的注册程序
    promise = {
        ClientTypeEnum.USER_EMAIL: __register_user_by_email,
        ClientTypeEnum.USER_MINA: __register_user_by_mina
    }
    promise[form.type.data]()
    return Success()

def __register_user_by_email():
    form = UserEmailForm().validate_for_api()
    User.register_by_email(form.nickname.data,
                            form.account.data,
                            form.secret.data)

def __register_user_by_mina():
    form = ClientForm().validate_for_api()
    wx_data = wx_get_user_by_code(form.account.data)
    User.register_by_mina(wx_data['openid'])