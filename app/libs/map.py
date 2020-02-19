# -*- coding: utf-8 -*-
"""
  Created by Wesley on 2020/2/7.
"""
import requests
from flask import current_app


def get_all_distance_from_tx_map(pos_from, pos_to):
    """
    从腾讯地图 api 获取距离
    :param pos_from: 
    :param pos_to: 
    :return: 
    """
    base_url = current_app.config['TX_MAP_GET_DISTANCE_BASE_URL']
    params = {
        'from': str(pos_from['latitude']) + ',' + str(pos_from['longitude']),
        'to': ';'.join([pos['latitude'] + ',' + pos['longitude'] for pos in pos_to]),
        'key': current_app.config['TX_MAP_KEY']
    }
    return requests.get(base_url, params).json()


def get_address_by_location_from_tx_map(lat, lng):
    """
    通过经纬度从腾讯地图 api 获取位置描述
    :param lat: 
    :param lng: 
    :return: 
    """
    base_url = current_app.config['TX_MAP_GET_ADDRESS_BASE_URL']
    params = {
        'location': str(lat) + ',' + str(lng),
        'key': current_app.config['TX_MAP_KEY']
    }

    return requests.get(base_url,params).json()



