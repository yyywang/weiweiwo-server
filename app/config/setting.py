# -*- coding: utf-8 -*-
"""
  Created by Wesley on 2019/12/30.
"""
import os

DEBUG = False
TOKEN_EXPIRATION = 2 * 3600
CACHE_TYPE = 'simple'

# 首页每页救助信息数量
RESCUE_LIST_PER_PAGE = 10
# 搜索结果每页展示数量
SEARCH_NUM_PER_PAGE = 10
ADMIN_QUERY_NUM = 10

# 腾讯地图相关
TX_MAP_GET_DISTANCE_BASE_URL = 'https://apis.map.qq.com/ws/distance/v1/'
TX_MAP_GET_ADDRESS_BASE_URL = 'https://apis.map.qq.com/ws/geocoder/v1/'

# 微信小程序相关
WX_LOGIN_BASE_URL = "https://api.weixin.qq.com/sns/jscode2session"
GET_TOKEN_BASE_URL = "https://api.weixin.qq.com/cgi-bin/token"
GET_WX_A_UNLIMIT_CODE_BASE_URL = "https://api.weixin.qq.com/wxa/getwxacodeunlimit"
SEND_SUBSCRIBE_MSG_BASE_URL = "https://api.weixin.qq.com/cgi-bin/message/subscribe/send"
MINIPROGRAM_STATE = "developer"
# developer为开发版；trial为体验版；formal为正式版；默认为正式版

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
wx_unlimit_code_dir = 'static' + os.sep + 'api' + os.sep + 'wx' + os.sep + 'unlimit_code' + os.sep
WX_UNLIMIT_CODE_DIR = os.path.join(basedir, wx_unlimit_code_dir)

# 好友助力速度
HIGH_SPEED = 8
MIDDLE_SPEED = 3
LOW_SPEED = 0

# -------- 用户相关 ---------- #
# 性别 0:未知；1:男性；2:女性
GENDER = {"value_list": (0,1,2),
          "des_list":("未知", "男性", "女性")}

# 个人查询数量
SEEK_HELP_PER_PAGE = 10
RESCUE_PER_PAGE = 10

SQLALCHEMY_TRACK_MODIFICATIONS = True
