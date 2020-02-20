# -*- coding: utf-8 -*-
"""
  Created by Wesley on 2020/2/10.
"""
from flask import current_app
from wtforms import StringField, PasswordField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Email, Regexp, length, ValidationError, URL, Length
from app.libs.error_code import ParameterException
from app.validators.base import BaseForm as Form
from app.libs.enums import ClientTypeEnum
from app.models.user import User


class ClientForm(Form):
    """微信小程序 code 从 account 参数传入"""
    account = StringField(validators=[DataRequired(message="不允许为空"), length(min=5, max=32)])
    secret = StringField()
    type = IntegerField(validators=[DataRequired()])

    def validate_type(self, value):
        try:
            # 判断用户传过来的数字是否是枚举类型的一种
            # 将数字转换为枚举类型，可读性强
            client = ClientTypeEnum(value.data)
        except ValueError as e:
            raise e
        self.type.data = client


class UserEmailForm(ClientForm):
    account = StringField(validators=[Email(message='invalidate email')])
    secret = StringField(validators=[
        DataRequired(),
        # 密码只能包含字母、数字和下划线
        Regexp(r'^[A-Za-z0-9_*&$#@]{6,22}$')
    ])
    nickname = StringField(validators=[
        DataRequired(),
        length(min=2, max=22)
    ])

    # 校验邮箱是否已被注册
    def validate_account(self, value):
        if User.query.filter_by(email=value.data).first():
            raise ValidationError(message="账号已注册")

class AdminLoginForm(Form):
    account = StringField(validators=[DataRequired(message='账号必填')])
    password = PasswordField(validators=[DataRequired(message='密码必填')])
    remember = BooleanField(default=False)


class WxLoginForm(ClientForm):
    wx_name = StringField(validators=[DataRequired()])
    wx_avatar = StringField(validators=[DataRequired(), URL()])


class TokenForm(Form):
    token = StringField(validators=[DataRequired()])


class UserUpdateForm(Form):
    wx_name = StringField(Length(max=128))
    wx_avatar = StringField(length(max=1000))
    gender = IntegerField()
    # !若未传任何参数，返回参数错误代码。在最后一个参数校验中写

    def validate_gender(self, value):
        # 校验性别参数是否正确
        if not value.data is None:
            gender_list = current_app.config['GENDER']
            if value.data not in gender_list['value_list']:
                raise ParameterException(msg='gender invalid')

        # 若未传任何参数，返回参数错误代码
        if self.wx_name.data is None and self.wx_avatar.data is None and value.data is None:
            raise ParameterException(msg='At least one parameter is required')


class UserSeekHelpListFrom(Form):
    page = IntegerField(default=1)