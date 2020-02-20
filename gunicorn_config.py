# -*- coding: utf-8 -*-
"""
  Created by Wesley on 2020/2/9.
"""
import multiprocessing

bind = '0.0.0.0:6666'
workers = multiprocessing.cpu_count() * 2 + 1