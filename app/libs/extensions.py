# -*- coding: utf-8 -*-
"""
  Created by Wesley on 2020/2/22.
"""
from flask_caching import Cache
from sqlalchemy.orm import Session

cache = Cache()
session = Session()
