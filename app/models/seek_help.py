# -*- coding: utf-8 -*-
"""
  Created by Wesley on 2020/2/7.
"""
from datetime import datetime
from flask import g
from sqlalchemy import Column, Integer, SmallInteger, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.models.base import Base, MixinJSONSerializer
from app.models.boost_seek_help import BoostSeekHelp


class SeekHelp(Base, MixinJSONSerializer):
    id = Column(Integer, primary_key=True)
    cat_num = Column(SmallInteger, default=0)
    dog_num = Column(SmallInteger, default=0)
    last_date = Column(Integer) # 最后喂养日期
    help_date = Column(Integer) # 需要帮助日期
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
    traffic_control = Column(SmallInteger) # 交通管控
    phone = Column(String(20))
    wx_id = Column(String(50))
    cancel = Column(Boolean, default=False) # 用户是否取消救助
    author_id = Column(Integer, ForeignKey('user.id'))
    update_logs = relationship('SeekHelpUpdateLog', backref='seek_help')
    error_feedbacks = relationship('ErrorFeedback', backref='seek_help') # 纠错
    boosts = relationship('BoostSeekHelp', backref='seek_help') # 助力信息


    def _set_fields(self):
        self._fields = ['id', 'cat_num', 'dog_num', 'last_date',
                        'help_date', 'support_days', 'traffic_ctrl',
                        'supplicant', 'location', 'rescued', 'speed', 'cancel']

    @property
    def traffic_ctrl(self):
        """
        0 - 外人可进
        1 - 本小区才可进
        :return: 
        """
        return "本小区才可进" if self.traffic_control else "小区外人可进"

    @property
    def position_dict(self):
        """返回字典形式的经纬度"""
        return {
            "latitude": self.latitude,
            "longitude": self.longitude
        }

    @property
    def support_days(self):
        """计算 = help_date - 今天"""
        result = datetime.utcfromtimestamp(self.help_date) - datetime.now()
        return result.days + 1

    @property
    def last_datetime(self):
        return datetime.fromtimestamp(self.last_date)

    @property
    def help_datetime(self):
        return datetime.fromtimestamp(self.help_date)

    @property
    def supplicant(self):
        """求助人信息"""
        return dict(
            id=self.author_id,
            phone=self.phone,
            wx_id=self.wx_id
        )

    @property
    def location(self):
        """求助地点"""
        return dict(
            province=self.province,
            city=self.city,
            district=self.district,
            address_name=self.address_name
        )

    @property
    def rescued(self):
        """是否被救助过。若有更新记录则视为救助过"""
        return True if len(self.update_logs) > 0 else False

    @property
    def speed(self):
        """加速人数"""
        return len(self.boosts)

    @property
    def helpers(self):
        """助力者"""
        returned = []
        for boost in self.boosts:
            returned.append(boost.helper)
        return returned

    @property
    def is_self(self):
        """判断是否是发布者打开加速页面"""
        return True if self.author_id == g.user.uid else False

    @property
    def has_help(self):
        """判断当前用户是否已助力"""
        return True if BoostSeekHelp.query.filter_by(
            seek_help_id=self.id, helper_id=g.user.uid).first() else False