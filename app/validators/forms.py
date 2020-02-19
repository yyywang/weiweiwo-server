# -*- coding: utf-8 -*-
"""
  Created by Wesley on 2019/12/31.
"""
import re
from wtforms import StringField, IntegerField, SelectField, FloatField, TextField
from wtforms.validators import DataRequired, Length
from app.libs.error_code import ParameterException
from app.validators.base import BaseForm as Form


class SeekHelpForm(Form):
    cat_num = IntegerField()
    dog_num = IntegerField()
    last_date = IntegerField(validators=[DataRequired()]) # 最后喂养日期
    help_date = IntegerField(validators=[DataRequired()]) # 需要帮助的日期
    address = StringField(validators=[DataRequired()]) # 详细地址
    latitude = StringField(validators=[DataRequired()]) # 纬度
    longitude = StringField(validators=[DataRequired()]) # 经度
    address_name = StringField(validators=[DataRequired()]) # 地址名
    traffic_control = SelectField(validators=[DataRequired()], choices=[('0', '外人可进'),('1', '本小区才可进')])
    phone = StringField(validators=[DataRequired()])
    wx_id = StringField(validators=[DataRequired()]) # 微信号


    def validate_dog_num(self, value):
        """校验 cat_num 与 dog_num 二者必填一个"""
        if not (value.data or self.cat_num.data):
            raise ParameterException(msg="dog_num or cat_num at least one is required")


    def validate_phone(self, value):
        """校验手机号是否正确"""
        reg = "1[3|4|5|7|8][0-9]{9}"
        if not re.findall(reg, value.data):
            raise ParameterException(msg='phone error')


class GetDataByLocationForm(Form):
    page = IntegerField(default=1) # 查询页数，默认为1
    province = StringField(default='全部')
    city = StringField(default='全部')
    district = StringField(default='全部')

    def validate_city(self, value):
        """若 city 传参，则 province 值不能为 ‘全部’ """
        if self.province.data == '全部' and value.data != '全部':
            raise ParameterException(msg="Incorrect param. Param <province> is required and not <全部>")

    def validate_district(self, value):
        """若 district 传参，则 province & city 值不能为 ‘全部’ """
        if value.data != '全部':
            if self.province.data == '全部':
                raise ParameterException(msg="Incorrect param. Param <province> is required and not <全部>")
            if self.city.data == '全部':
                raise ParameterException(msg="Incorrect param. Param <city> is required and not <全部>")


class GetRescueByDistanceForm(Form):
    latitude = StringField(validators=[DataRequired()]) # 纬度
    longitude = StringField(validators=[DataRequired()]) # 经度
    page = IntegerField(default=1)


class RescueSearchForm(Form):
    q = StringField(validators=[DataRequired()])
    page = IntegerField(default=1)


class ErrorFeedbackForm(Form):
    err_type = SelectField(validators=[DataRequired()], choices=[
        ('0', '联系不上宠物主'),('1', '宠物已不需要帮助'),('2', '信息重复'),('3', '其他')])
    msg_id = IntegerField(validators=[DataRequired()])


class UpdateSeekHelpForm(Form):
    last_date = IntegerField(validators=[DataRequired()])
    help_date = IntegerField(validators=[DataRequired()])

    # def validate_end_date(self, value):
    #     """end_date 与 support_days 至少填一个"""
    #     if not (self.support_days.data  or value.data):
    #         raise ParameterException('end_date or support_days at least one is required')


class RescueForm(Form):
    address = StringField(validators=[DataRequired()])  # 详细地址
    latitude = StringField(validators=[DataRequired()])  # 纬度
    longitude = StringField(validators=[DataRequired()])  # 经度
    address_name = StringField(validators=[DataRequired()])  # 地址名
    help_range = IntegerField(validators=[DataRequired()]) # 能帮范围
    cost = IntegerField(default=0) # 收费费用
    phone = StringField(validators=[DataRequired()])
    wx_id = StringField(validators=[DataRequired()])  # 微信号
    note = StringField(validators=[Length(max=50)])


    def validate_help_range(self, value):
        if value.data < 0:
            raise ParameterException(msg='help_range must be not less than 0')

    def validate_cost(self, value):
        if value.data < 0:
            raise ParameterException(msg='cost must be not less than 0')

    def validate_phone(self, value):
        """校验手机号是否正确"""
        reg = "1[3|4|5|7|8][0-9]{9}"
        if not re.findall(reg, value.data):
            raise ParameterException(msg='phone error')