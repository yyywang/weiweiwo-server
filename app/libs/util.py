# -*- coding: utf-8 -*-
"""
  Created by Wesley on 2020/2/21.
"""
def dict_rm_none(data):
    """将字典中值为 None 的键值对剔除"""
    for key in list(data.keys()):
        if data.get(key) is None:
            del data[key]

    return data