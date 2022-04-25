# -*- coding: UTF-8 -*-

host = '127.0.0.1'
port = 3306
database_name = 'douban_film_analysis'
username = 'root'
password = '123456'


class DatabaseConfig:
    """
        MySQL数据库相关设置
    """
    SQLALCHEMY_DATABASE_URI = 'mysql://' + username + ":" + password + "@" + host + ":" + str(
        port) + "/" + database_name
    # 每次请求结束后都会自动提交数据库中的变动
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    # 动态追踪修改设置，如未设置只会提示警告
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # SQLAlchemy 会记录所有 发给 stderr 的语句
    SQLALCHEMY_ECHO = True
    # 可以用于显式地禁用或启用查询记录. 在调试或测试模式自动启用
    SQLALCHEMY_RECORD_QUERIES = True
