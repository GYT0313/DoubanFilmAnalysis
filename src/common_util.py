# -*- coding: UTF-8 -*-


import datetime as dt
from datetime import datetime

"""
通用公共工具方法
"""


def get_date_by_standard_time(standard_time):
    """
    将yyyy-MM-DD HH:mm:ss格式的时间返回年月日
    :param standard_time:
    :return:
    """
    return datetime.strptime(standard_time, '%Y-%m-%d %H:%M:%S').date().__str__()


def get_standard_time_by_date_time(date_time):
    """
    根据年-月-日 返回 年-月-日 00:00:00
    :param date_time:
    :return:
    """
    return datetime.strptime(date_time, '%Y-%m-%d').__str__()


def get_standard_time(standard_time):
    """
    返回格式化时间
    :return:
    """
    return datetime.strptime(standard_time, '%Y-%m-%d %H:%M:%S')


def time_plus_one_day(date_time):
    """
    时间+1天
    :param date_time:  2022-03-10
    :return:
    """
    return get_standard_time(get_standard_time_by_date_time(date_time)) + dt.timedelta(days=1)


def get_feature_time(date_time, few_days):
    """
    返回未来一共few_days 天
    :param date_time:
    :param few_days:
    :return:
    """
    res = [get_standard_time_by_date_time(date_time)]
    for i in range(few_days):
        res.append(str(time_plus_one_day(get_date_by_standard_time(res[i]))))
    return res[1:]
