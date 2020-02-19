# -*- coding: utf-8 -*-
"""
  Created by Wesley on 2020/2/9.
"""
import multiprocessing

bind = '127.0.0.1:5009'
workers = multiprocessing.cpu_count() * 2 + 1