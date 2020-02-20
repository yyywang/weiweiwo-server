# -*- coding: utf-8 -*-
"""
  Created by Wesley on 2020/2/20.
"""
from http.client import HTTPException

import requests

GET_TOKEN_BASE_URL = "https://api.weixin.qq.com/cgi-bin/token"

def get_access_token():
    params = {
        "grant_type": "client_credential",
        "appid": "wx9298aaee95eb4726",
        "secret": "bf7e244c84cc6ce64e1c0b561c36ea91"
    }

    try:
        response = requests.post(GET_TOKEN_BASE_URL, params).json()
    except HTTPException:
        raise
    # while response.json()

    a = 1

get_access_token()