# -*- coding: utf-8 -*-
"""
  Created by Wesley on 2020/2/7.
"""
import math
from flask import current_app, g
from app.libs.error_code import Success, DeleteSuccess
from app.libs.extensions import cache, session
from app.libs.map import get_address_by_location_from_tx_map, get_all_distance_from_tx_map
from app.libs.redprint import Redprint
from app.libs.statistics import get_boost_data
from app.libs.token_auth import auth
from app.models.base import db
from app.models.boost_seek_help import BoostSeekHelp
from app.models.error_feedback import ErrorFeedback
from app.models.seek_help import SeekHelp
from app.models.seek_help_update_log import SeekHelpUpdateLog
from app.models.user import User
from app.validators.forms import SeekHelpForm, GetDataByLocationForm, GetRescueByDistanceForm, UpdateSeekHelpForm, \
    ErrorFeedbackForm

api = Redprint("seek-help")


@api.route('', methods=['POST'])
@auth.login_required
def seek_help():
    """发布求助信息"""
    form = SeekHelpForm().validate_for_api()
    # 通过经纬度从腾讯地图获得位置描述：省/市/区
    location = get_address_by_location_from_tx_map(form.latitude.data, form.longitude.data)
    with db.auto_commit():
        obj_seek_help = SeekHelp()
        obj_seek_help.set_attrs(form.data)
        obj_seek_help.set_attrs(location['result']['address_component'])
        obj_seek_help.author_id = g.user.uid
        db.session.add(obj_seek_help)
    return Success(data={"id": obj_seek_help.id})


@api.route('/<int:sid>')
@auth.login_required
def get_seek_help(sid):
    """返回 id=sid 的 SeekHelp"""
    obj_seek_help = SeekHelp.query.filter_by(id=sid, cancel=False).first_or_404()
    return Success(data=obj_seek_help)


@api.route('/location')
@auth.login_required
@cache.cached(query_string=True) # 默认缓存过期时间为 300s
def get_shs_by_location():
    """获取 求助 数据列表，根据 省/市/区 筛选

    params: 
        *<int:page> 第几页
        *<str:province> 省
        *<str:city> 市
        *<str:district> 区
    """
    form = GetDataByLocationForm().validate_for_api()
    per_page = current_app.config['RESCUE_LIST_PER_PAGE']

    if form.province.data == "全部":
        all_shs = SeekHelp.query.filter_by(cancel=False).all()
    elif form.city.data == "全部":
        all_shs = SeekHelp.query.filter_by(cancel=False, province=form.province.data).all()
    elif form.district.data == "全部":
        all_shs = SeekHelp.query.filter_by(cancel=False, province=form.province.data, city=form.city.data).all()
    else:
        # 按 省/市/区 筛选
        all_shs = SeekHelp.query.filter_by(
            cancel=False, province=form.province.data, city=form.city.data, district=form.district.data).all()

    all_shs = __sort_sh_by_speed(all_shs, reverse=True) # 将数据按 speed 降序排序
    pagination = __pagination_seek_help(all_shs, page=form.page.data, per_page=per_page)

    return Success(data=pagination)


@api.route('/distance')
@auth.login_required
def get_shs_by_distance():
    """根据用户定位获取 求助 数据列表
    按高速、中速、低速排列，
    相同状态下，按计算排序值=0.4*可支撑天数+0.6*距离，按从小到大排序

    params:
        <str:latitude> 纬度
        <str:longitude> 经度
    """
    form = GetRescueByDistanceForm().validate_for_api()
    pos_from = {
        "latitude": form.latitude.data,
        "longitude": form.longitude.data
    }
    shs = __sort_index_sh(pos_from)
    per_page = current_app.config['RESCUE_LIST_PER_PAGE']
    returned = __pagination_seek_help(shs, page=int(form.page.data), per_page=per_page)
    return Success(data=returned)


@api.route('/<int:sid>', methods=['PUT'])
@auth.login_required
def update_seek_help(sid):
    """
    更新 id=sid 的 SeekHelp
    :param sid: id of SeekHelp
    :return: APIException
    """
    form = UpdateSeekHelpForm().validate_for_api()
    obj_seek_help = SeekHelp.query.filter_by(id=sid).first_or_404()
    with db.auto_commit():
        # 日志记录
        obj_seek_help_update_log = SeekHelpUpdateLog()
        obj_seek_help_update_log.operator_id = g.user.uid
        obj_seek_help_update_log.seek_help_id = obj_seek_help.id
        obj_seek_help_update_log.old_help_date = obj_seek_help.help_date
        obj_seek_help_update_log.new_help_date = form.help_date.data
        obj_seek_help_update_log.old_last_date = obj_seek_help.last_date
        obj_seek_help_update_log.new_last_date = form.last_date.data
        db.session.add(obj_seek_help_update_log)

        # 更新 seek_help 数据
        obj_seek_help.last_date = form.last_date.data
        obj_seek_help.help_date = form.help_date.data

        db.session.add(obj_seek_help)
    return Success()


@api.route('/error', methods=['POST'])
@auth.login_required
def create_error_feedback():
    """创建错误反馈"""
    form = ErrorFeedbackForm().validate_for_api()
    with db.auto_commit():
        obj_error_feedback = ErrorFeedback()
        obj_error_feedback.set_attrs(form.data)
        obj_error_feedback.author_id = g.user.uid
        db.session.add(obj_error_feedback)
    return Success()


@api.route('/<int:sid>/boost', methods=['POST'])
@auth.login_required
def boost_seek_help(sid):
    """
    好友助力
    :param sid: id of SeekHelp
    :return: APIException
    """
    obj_seek_help = SeekHelp.query.filter_by(cancel=False, id=sid).first_or_404()
    obj_user = User.query.filter_by(id=g.user.uid).first_or_404()

    obj_user.verify_boost(obj_seek_help) # 校验用户能否助力此 seek_help

    with db.auto_commit():
        obj_boost_seek_help = BoostSeekHelp()
        obj_boost_seek_help.helper_id = obj_user.id
        obj_boost_seek_help.seek_help_id = obj_seek_help.id
        db.session.add(obj_boost_seek_help)
    return Success()


@api.route('/<int:sid>/boost')
@auth.login_required
def get_boost_seek_help(sid):
    """
    获取某助力信息
    :param sid: id of SeekHelp
    :return: 
    """
    obj_seek_help = SeekHelp.query.filter_by(cancel=False, id=sid).first_or_404()

    if obj_seek_help.is_self:
        obj_seek_help.append('helpers')
    else:
        obj_seek_help.append('has_help')
        if obj_seek_help.has_help:
            obj_seek_help.append('helpers')

    obj_seek_help.statistics = get_boost_data() # 平台人数
    obj_seek_help.append('is_self', 'statistics')  # 返回字段中加入 是否是发布者打开页面
    obj_seek_help.hide('rescued')
    return Success(data=obj_seek_help)


# 后台接口
@api.route('/<int:id>', methods=['DELETE'])
def delete_seek_help(id):
    """删除 id=id 的 SeekHelp"""
    obj_seek_help = SeekHelp.query.filter_by(id=id).first_or_404()
    with db.auto_commit():
        obj_seek_help.delete()
    return DeleteSuccess()


def __get_pos_list(data):
    """将所有 SeekHelp 中的单个经纬度提取到一个列表中"""
    pos_list = []
    for pos in data:
        pos_list.append(pos.position_dict)
    return pos_list


def __sort_index_sh(pos_from):
    """
    首页数据排序
    按高速、中速、低速排列，
    相同状态下，按计算排序值=0.4*可支撑天数+0.6*距离，按从小到大排序。
    :param pos_from: 
    :return: 
    """
    seek_help_list = SeekHelp.query.filter_by(cancel=False).all()[:20]
    all_shs = get_shs_by_level(seek_help_list) # 按助力等级分类

    # 同一状态内数据排序
    high_shs = __sort_sh_by_dis_and_day(all_shs['high_shs'], pos_from)
    middle_shs = __sort_sh_by_dis_and_day(all_shs['middle_shs'], pos_from)
    low_shs = __sort_sh_by_dis_and_day(all_shs['low_shs'], pos_from)

    return high_shs + middle_shs + low_shs


def get_shs_by_level(seek_help_list):
    """
    通过助力级别分类 SeekHelp
    :param seek_help_list: 
    :return: 
    """
    high_shs = list()
    middle_shs = list()
    low_shs = list()

    for sh in seek_help_list:
        if sh.speed >= current_app.config['HIGH_SPEED']:
            high_shs.append(sh)
        elif sh.speed >= current_app.config['MIDDLE_SPEED']:
            middle_shs.append(sh)
        else:
            low_shs.append(sh)

    return dict(
        high_shs=high_shs,
        middle_shs=middle_shs,
        low_shs=low_shs
    )


def __sort_sh_by_dis_and_day(seek_help_list, pos_from):
    """
    计算 = 0.6*距离+0.4*可支撑天数
    按计算结果从小到大排序
    :param seek_help_list: 
    :return: 
    """
    # 若列表元素 < 2 则不进行排序
    if len(seek_help_list) < 2:
        return seek_help_list

    pos_to = __get_pos_list(seek_help_list)
    # 从腾讯地图接口获取用户当前位置到各位置距离
    distance_list = get_all_distance_from_tx_map(pos_from, pos_to)

    # 将距离数据添加至 seek_help 类中
    for idx, sh in enumerate(seek_help_list):
        sh.distance = distance_list['result']['elements'][idx]['distance']

    for sh in seek_help_list:
        sh.sort_score = 0.6 * (sh.distance / 1000) + 0.4 * sh.support_days
        sh.append('distance') # 添加额外序列化字段

    # 通过计算得出的排序分进行升序排序
    seek_help_list.sort(key=lambda sh: sh.sort_score, reverse=False)
    return seek_help_list


def __sort_sh_by_speed(shs, reverse=False):
    """通过等级排序 SeekHelp"""
    shs.sort(key=lambda  sh: sh.speed, reverse=reverse)
    return shs


def __pagination_seek_help(seek_help_list, page=1 ,per_page=10):
    """将按距离排序的 SeekHelp 分页返回"""
    pages = int(math.ceil(len(seek_help_list) / per_page))
    page = int(page)
    per_page = int(per_page)

    # if page > pages:
    #     raise ParameterException('page out range')

    has_next = True if pages > page else False
    has_prev = True if 1 < page <= int(pages) else False
    items = seek_help_list[(page-1)*per_page : page*per_page]
    # for item in items:
    #     session.merge(item)

    return {
        "items": items,
        "page": page,
        "total": len(seek_help_list),
        "pages": pages,
        "has_next": has_next,
        "next_num": page + 1 if has_next else None,
        "per_page": per_page,
        "has_prev": has_prev,
        "prev_num": page - 1 if has_prev else None
    }