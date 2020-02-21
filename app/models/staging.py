# -*- coding: utf-8 -*-
"""
  Created by Wesley on 2020/2/20.
"""
from datetime import datetime

from sqlalchemy import Column, Integer, String
from app.models.base import Base


class Staging(Base):
    """暂存"""
    id = Column(Integer,primary_key=True)
    key = Column(String(20)) # 暂存的键
    value = Column(String(1000)) # 暂存的值
    expires_at = Column(Integer) # 过期时间
    des = Column(String(100)) # 暂存值的描述

    def is_expire(self):
        """校验是否过期"""
        return True if self.expires_at < int(datetime.now().timestamp()) else False
