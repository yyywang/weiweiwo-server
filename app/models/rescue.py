# -*- coding: utf-8 -*-
"""
  Created by Wesley on 2020/2/19.
"""
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from app.models.base import MixinJSONSerializer, Base


class Rescue(Base, MixinJSONSerializer):
    id = Column(Integer, primary_key=True)
    nation = Column(String(50)) # 国家
    province = Column(String(50)) # 省
    city = Column(String(50)) # 市
    district = Column(String(50)) # 区
    street = Column(String(255)) # 街道
    street_number = Column(String(255)) # 门牌号
    address = Column(String(255)) # 详细地址
    latitude = Column(String(50)) # 纬度
    longitude = Column(String(50)) # 经度
    address_name = Column(String(50)) # 地址名称
    help_range = Column(Integer) # 愿意帮的范围，单位：米
    cost = Column(Integer) # 帮一次收费，单位：元
    phone = Column(String(20)) # 手机号
    wx_id = Column(String(50))
    note = Column(String(100)) # 备注
    author_id = Column(Integer, ForeignKey('user.id'))
    cancel = Column(Boolean, default=False) # 用户是否取消我能帮信息


    def _set_fields(self):
        self._fields = ['id', 'note', 'help_range', 'cost', 'location', 'rescuer', 'wx_id', 'phone']

    @property
    def location(self):
        return dict(
            province=self.province,
            city=self.city,
            district=self.district,
            address_name=self.address_name
        )

    @property
    def rescuer(self):
        return self.author