# -*- coding: utf-8 -*-
"""
  Created by Wesley on 2020/2/22.
"""
import uuid
from datetime import datetime


def get_random_filename():
    filename = datetime.now().strftime("%Y%m%d%H%M%S") + str(uuid.uuid4().hex)
    return filename