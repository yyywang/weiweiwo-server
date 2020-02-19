# -*- coding: utf-8 -*-
"""
  Created by Wesley on 2020/2/8.
"""

def process_rsp_pagination(pagination):
    """
    处理要返回的，单个 pagination 的数据，以支持序列化
    :param pagination: 
    :return: 
    """
    return {
        "has_next": pagination.has_next,
        "has_prev": pagination.has_prev,
        "next_num": pagination.next_num,
        "page": pagination.page,
        "pages": pagination.pages,
        "per_page": pagination.per_page,
        "prev_num": pagination.prev_num,
        "total": pagination.total,
        "items":pagination.items
    }