# -*- coding: UTF-8 -*-
import json
from datetime import timedelta

import pymysql
from flask import Flask
from flask import redirect, url_for
from flask import render_template
from flask_sqlalchemy import SQLAlchemy

from src import database_config
from src import spider_film

# 加上才能正确运行
pymysql.install_as_MySQLdb()

# app
app = Flask(__name__)

# MySQL数据库相关设置
app.config.from_object(database_config.DatabaseConfig)
db = SQLAlchemy(app)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=3)


@app.route('/', methods=['GET'])
def home():
    return redirect(url_for('index'))


@app.route('/index', methods=['GET'])
def index():
    return render_template("index.html")


# ##################################################################################
@app.route('/film/language/top', methods=['GET'])
def get_film_language_top():
    """
    电影语言top
    :return:
    """
    string = """
        [
            {
                "language": "普通话",
                "total": 1
            },
            {
                "language": "英语",
                "total": 2
            },
            {
                "language": "日语",
                "total": 3
            },
            {
                "language": "韩语",
                "total": 4
            },
            {
                "language": "俄语",
                "total": 5
            },
            {
                "language": "粤语",
                "total": 6
            }
        ]
    """
    return json.dumps(json.loads(string))

@app.route('/film/score/length/relation', methods=['GET'])
def get_score_length_relation():
    """
    评分-时长关系
    :return:
    """
    string = """
[
  {
    "length": 114,
    "score": 1.5
  },
  {
    "length": 100,
    "score": 2.4
  },
  {
    "length": 33,
    "score": 3.6
  },
  {
    "length": 67,
    "score": 9.5
  }
]
    """
    return json.dumps(json.loads(string))


@app.route('/film/director/films', methods=['GET'])
def get_director_films():
    """
    导演电影数量Top n
    :return:
    """
    string = """
[
  {
    "name": "小明",
    "total": 20
  },
  {
    "name": "小黄",
    "total": 1
  },
  {
    "name": "小王",
    "total": 11
  },
  {
    "name": "小李",
    "total": 5
  }
]
    """
    return json.dumps(json.loads(string))


# @app.route('/pull/film', methods=['GET'])
# def pull_film():
#     """
#     拉取电影
#     :return:
#     """
#     return spider_film.pull_film(db, Film, FilmInformation, Director, Performer, FilmType)


# ##################################################################################
@app.route('/pull/film', methods=['GET'])
def pull_film():
    """
    拉取电影
    :return:
    """
    return spider_film.pull_film(db, Film, FilmInformation, Director, Performer, FilmType)


# #############################################################################################

# class Jobs(object):
#     """
#     定时任务
#     """
#
#     @staticmethod
#     def pull_global():
#         """
#         从腾讯API拉取全球数据并保持
#         :return:
#         """
#         is_add_or_update = tencent_request_service.save_global_data(
#             db=db,
#             GlobalWomWorld=GlobalWomWorld,
#             GlobalWomAboard=GlobalWomAboard,
#             GlobalDaily=GlobalDaily)
#         db.session.close()
#         return is_add_or_update
#
#     @staticmethod
#     def pull_china():
#         """
#         从腾讯API拉取国内数据并保持
#         :return:
#         """
#         is_add_or_update = tencent_request_service.save_china(
#             db,
#             ChinaTotal=ChinaTotal,
#             ChinaCompareDaily=ChinaCompareDaily,
#             ChinaProvince=ChinaProvince,
#             ChinaCity=ChinaCity)
#         db.session.close()
#         return is_add_or_update


def app_init():
    """
        初始化app
    :return:
    """
    # 不启用ASCII
    app.config['JSON_AS_ASCII'] = False

    # print(database_config.DatabaseConfig.SQLALCHEMY_DATABASE_URI)


def get_app():
    return app


# def get_db():
#     return db


# #################################模型类#####################################

class Film(db.Model):
    """
    分页下电影模型
    """
    __tablename__ = 't_film'
    id = db.Column(db.Integer, primary_key=True, comment='主键')
    name = db.Column(db.String(128), comment='电影名称')
    subject_id = db.Column(db.String(128), comment='电影id', index=True)
    url = db.Column(db.String(128), comment='电影信息url')
    status = db.Column(db.String(128), comment='是否已拉取电影信息: 是-否')

    def __self_dict__(self):
        """
        返回所有属性的字典
        :return:
        """
        return {
            'id': self.id,
            'name': self.name,
            'subject_id': self.subject_id,
            'url': self.url,
            'status': self.status
        }


class FilmInformation(db.Model):
    """
    电影信息模型
    """
    __tablename__ = 't_film_information'
    id = db.Column(db.Integer, primary_key=True, comment='主键')
    name = db.Column(db.String(128), comment='电影名称')
    subject_id = db.Column(db.String(128), comment='电影id', index=True)
    score = db.Column(db.Float, comment='评分')
    country_or_region = db.Column(db.String(128), comment='国家/地区')
    language = db.Column(db.String(128), comment='语言')
    release_date = db.Column(db.String(128), comment='上映日期')
    year = db.Column(db.String(128), comment='所在年')
    film_length = db.Column(db.String(128), comment='片长')

    def __self_dict__(self):
        """
        返回所有属性的字
        :return:
        """
        return {
            'id': self.id,
            'name': self.name,
            'subject_id': self.subject_id,
            'score': self.score,
            'country_or_region': self.country_or_region,
            'language': self.language,
            'release_date': self.release_date,
            'year': self.year,
            'film_length': self.film_length
        }


class Director(db.Model):
    """
    导演模型
    """
    __tablename__ = 't_director'
    id = db.Column(db.Integer, primary_key=True, comment='主键')
    name = db.Column(db.String(128), comment='导演姓名')

    film_information_id = db.Column(
        db.Integer,
        db.ForeignKey('t_film_information.id'),
        comment='外键到电影信息表')
    # 使用此字段可以直接查询外键关联的film_information
    film_information = db.relationship('FilmInformation', backref=db.backref('director'))

    def __self_dict__(self):
        """
        返回所有属性的字典
        :return:
        """
        return {
            'id': self.id,
            'name': self.name,
            'film_information_id': self.film_information_id
        }


class Performer(db.Model):
    """
    演员模型
    """
    __tablename__ = 't_performer'
    id = db.Column(db.Integer, primary_key=True, comment='主键')
    name = db.Column(db.String(128), comment='演员姓名')

    film_information_id = db.Column(
        db.Integer,
        db.ForeignKey('t_film_information.id'),
        comment='外键到电影信息表')
    # 使用此字段可以直接查询外键关联的film_information
    film_information = db.relationship('FilmInformation', backref=db.backref('performer'))

    def __self_dict__(self):
        """
        返回所有属性的字典
        :return:
        """
        return {
            'id': self.id,
            'name': self.name,
            'film_information_id': self.film_information_id
        }


class FilmType(db.Model):
    """
    电影类型模型
    """
    __tablename__ = 't_film_type'
    id = db.Column(db.Integer, primary_key=True, comment='主键')
    name = db.Column(db.String(128), comment='类型名称')

    film_information_id = db.Column(
        db.Integer,
        db.ForeignKey('t_film_information.id'),
        comment='外键到电影信息表')
    # 使用此字段可以直接查询外键关联的film_information
    film_information = db.relationship('FilmInformation', backref=db.backref('film_type'))

    def __self_dict__(self):
        """
        返回所有属性的字典
        :return:
        """
        return {
            'id': self.id,
            'name': self.name,
            'film_information_id': self.film_information_id
        }


# ###############################################################################

def table_init():
    """
    表结构初始化
    :return:
    """
    db.drop_all()
    db.create_all()
    db.session.commit()


if __name__ == '__main__':
    # app初始化
    app_init()
    # MySQL表初始化
    # table_init()

    app.run(debug=True, use_reloader=False, port=5001)
