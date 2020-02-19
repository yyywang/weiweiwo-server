# -*- coding: utf-8 -*-
"""
  Created by Wesley on 2019/12/31.
"""

from enum import Enum

class ClientTypeEnum(Enum):
    # 普通用户赋值为1开头的数字（习惯用法）
    USER_EMAIL = 100
    USER_MOBILE = 101
    # 微信系列的赋值为2开头的数字（习惯用法）
    USER_MINA = 200 # 微信小程序
    USER_WX = 201 # 微信公众号