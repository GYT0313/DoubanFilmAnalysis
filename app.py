# -*- coding: UTF-8 -*-
import json
import os
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


def get_project_path():
    """
    获取项目绝对路径
    :return:
    """
    # 项目名称
    p_name = 'DoubanFilmAnalysis'
    # 获取当前文件的绝对路径
    p_path = os.path.abspath(os.path.dirname(__file__))
    # 通过字符串截取方式获取
    return p_path[:p_path.index(p_name) + len(p_name)]


project_path = get_project_path()


def read_json(file_name):
    """
    读取json文件
    :param file_name:
    :return:
    """
    return json.load(open(project_path + "\\static\json\\" + file_name, 'r', encoding="utf-8"))


# ##################################################################################
@app.route('/film/language/top', methods=['GET'])
def get_film_language_top():
    """
    电影语言top
    :return:
    """
    # 读静态json
    return json.dumps(read_json("language_top_10.json"), ensure_ascii=False)

    # # sql查, pandas处理
    # film_information_all = FilmInformation.query.all()
    # film_language_top = pd.DataFrame(list(map(lambda x: x.__self_dict__(), film_information_all)))[
    #                         "language"].value_counts().sort_values(ascending=False)[:10]
    # # 数据处理
    # film_language_top = film_language_top.reset_index()
    # film_language_top["total"] = film_language_top["language"]
    # film_language_top["name"] = film_language_top["index"]
    #
    # return film_language_top.to_json(orient="records")


@app.route('/film/score/length/relation', methods=['GET'])
def get_score_length_relation():
    """
    评分-时长关系
    :return:
    """
    # 读静态json
    return json.dumps(read_json("score_length.json"), ensure_ascii=False)

    # # sql查, pandas处理
    # film_information_all = FilmInformation.query.all()
    # film_information_pd = pd.DataFrame(list(map(lambda x: x.__self_dict__(), film_information_all)))
    # # 数据处理
    # res = pd.DataFrame()
    # res["length"] = film_information_pd["film_length"]
    # res["score"] = film_information_pd["score"]
    # res = res.replace(['', ' ', 'None', None, 'NULL', 'null', 'Null'], numpy.nan).dropna()
    # res["length"] = res["length"].apply(pd.to_numeric, errors='coerce')
    # # 排序、过滤评分为0的
    # res = res.sort_values(by="length", ascending=False)
    # res = res[res["score"] != 0]
    #
    # return res.to_json(orient="records")


@app.route('/film/director/films', methods=['GET'])
def get_director_films():
    """
    导演电影数量Top n
    :return:
    """
    # 读静态json
    return json.dumps(read_json("director_top_10.json"), ensure_ascii=False)

    # # sql查, pandas处理
    # director_all = Director.query.all()
    # director_top = pd.DataFrame(list(map(lambda x: x.__self_dict__(), director_all)))[
    #                    "name"].value_counts().sort_values(ascending=False)[:10]
    # # 数据处理
    # director_top = director_top.reset_index()
    # director_top["total"] = director_top["name"]
    # director_top["name"] = director_top["index"]
    #
    # return director_top.to_json(orient="records")


@app.route('/film/type', methods=['GET'])
def get_film_type():
    """
    电影类型
    :return:
    """
    # 读静态json
    return json.dumps(read_json("film_type.json"), ensure_ascii=False)

    # # sql查, pandas处理
    # film_type_all = FilmType.query.all()
    # film_type_top = pd.DataFrame(list(map(lambda x: x.__self_dict__(), film_type_all)))[
    #     "name"].value_counts().sort_values(ascending=False)
    # # 数据处理
    # film_type_top = film_type_top.reset_index()
    # film_type_top['value'] = film_type_top['name']
    # film_type_top["name"] = film_type_top["index"]
    #
    # return film_type_top.to_json(orient="records")


@app.route('/film/country/count', methods=['GET'])
def get_film_country_count():
    """
    各国电影计数
    :return:
    """
    # 读静态json
    return json.dumps(read_json("country_or_region_count.json"), ensure_ascii=False)

    # # sql查, pandas处理
    # film_information_all = FilmInformation.query.all()
    # film_country_or_region_top = pd.DataFrame(list(map(lambda x: x.__self_dict__(), film_information_all)))[
    #                                  "country_or_region"].value_counts().sort_values(ascending=False)
    # # 数据处理
    # film_country_or_region_top = film_country_or_region_top.reset_index()
    # film_country_or_region_top["total"] = film_country_or_region_top["country_or_region"]
    # film_country_or_region_top["name"] = film_country_or_region_top["index"]
    #
    # return film_country_or_region_top.to_json(orient="records")


@app.route('/film/statistics', methods=['GET'])
def get_film_statistics():
    """
    电影数量统计
    :return:
    """
    # 读静态json
    return json.dumps(read_json("statistics.json"), ensure_ascii=False)

    # # sql查, pandas处理
    # film_information_all = FilmInformation.query.all()
    # director_all = Director.query.all()
    # performer_all = Performer.query.all()
    # film_type_all = FilmType.query.all()
    # # 数据处理
    # film_total = int(len(film_information_all))
    # country_total = int(len(
    #     list(set(list(map(lambda film_information: film_information.country_or_region, film_information_all))))))
    # film_type_total = int(len(list(set(list(map(lambda film_type: film_type.name, film_type_all))))))
    # director_total = int(len(list(set(list(map(lambda director: director.name, director_all))))))
    # performer_total = int(len(list(set(list(map(lambda performer: performer.name, performer_all))))))
    #
    # return json.dumps({
    #     "film_total": film_total,
    #     "country_total": country_total,
    #     "film_type_total": film_type_total,
    #     "director_total": director_total,
    #     "performer_total": performer_total
    # })


# ##################################################################################
@app.route('/pull/film', methods=['GET'])
def pull_film():
    """
    拉取电影
    :return:
    """
    return spider_film.pull_film(db, Film, FilmInformation, Director, Performer, FilmType)


# #############################################################################################


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
