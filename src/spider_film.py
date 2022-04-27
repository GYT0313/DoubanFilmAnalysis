# -*- coding: UTF-8 -*-

"""
爬取豆瓣电影信息
"""
import json
import math
import time

import requests
import unicodedata
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from sqlalchemy import and_

base_url = "https://movie.douban.com"

film_url = "/j/new_search_subjects?sort=U&range=0,10&tags=&start=%s"

# film状态
film_status = {
    "pull": "是",
    "not_pull": "否"
}


def request(url):
    """
    请求第三方API
    :param url: API
    :return: 三方API响应
    """
    return requests.get(url=url, headers={
        'User-Agent': UserAgent().random
    })


def request_film(start_num):
    """
    请求分类下的电影
    :return:
    """
    url = base_url + (film_url % start_num)
    return json.loads(request(url).text)


def request_film_information(url):
    """
    请求电影信息
    :param url:
    :return:
    """
    return request(url).text


def save_film(db, Film, film_json):
    """
    保存电影列表
    :return:
    """
    film = Film(
        name=film_json.get("title"),
        subject_id=film_json.get("id"),
        url=film_json.get("url"),
        status=film_status.get("not_pull")
    )
    film_mysql_list = Film.query.filter(Film.subject_id == film.subject_id).all()
    if len(film_mysql_list) <= 0:
        db.session.add(film)
        db.session.commit()
        film_in_mysql = Film.query.filter(Film.subject_id == film.subject_id).all()[0]
        return [film_in_mysql.subject_id, film_in_mysql.url]
    if len(film_mysql_list) == 1 and film_mysql_list[0].status == film_status.get("not_pull"):
        return [film_mysql_list[0].subject_id, film_mysql_list[0].url]

    return None


def save_film_information(db, subject_id, FilmInformation, film_html):
    """
    保存电影信息
    :return:
    """
    soup = process_html(film_html)
    info = get_info(soup)
    film_information = FilmInformation(
        name=soup.find("h1").find("span").text,
        subject_id=subject_id,
        score=float(soup.find("strong", class_="rating_num").text) if is_number(
            soup.find("strong", class_="rating_num").text) else 0,
        country_or_region=get_text_by_info(info, "制片国家/地区"),
        language=get_text_by_info(info, "语言"),
        release_date=get_text_by_info(info, "上映日期"),
        year=soup.find("span", class_="year").text.replace("(", "").replace(")", ""),
        film_length=get_text_by_info(info, "片长")
    )
    film_information_list = FilmInformation.query.filter(
        FilmInformation.subject_id == film_information.subject_id).all()
    if len(film_information_list) <= 0:
        db.session.add(film_information)
        db.session.commit()
        film_information_in_mysql = FilmInformation.query.filter(
            FilmInformation.subject_id == film_information.subject_id).all()[0]
        return film_information_in_mysql.id
    return None


def get_info(soup):
    """
    获取info
    :return:
    """
    return soup.find("div", class_="subject").find("div", id="info").text \
        .replace(" ", "").split("\n")


def get_text_by_info(info, flag):
    """
    从info获取指定字段的内容
    :return:
    """
    result = None
    for text in info:
        if flag in text:
            result = text.split(":")[1]

    if result is not None:
        if flag == "上映日期":
            result = result[0:9]
            if "(" in result:
                result = result.split("(")[0] + "-01-01"
        elif flag == "片长":
            temp = ""
            for char in result.split("/")[0].split("-")[0].split("分钟")[0].split("分")[0]:
                if char.isdigit():
                    temp += char
            result = temp
        elif flag == "制片国家/地区":
            if len(result) >= 1 and "/" in result:
                result = result.split("/")[0]
            if "中国" in result:
                for name in ["大陆", "香港", "澳门", "台湾"]:
                    if name in result:
                        result = "中国"
                        break
        elif flag == "语言":
            if len(result) >= 1 and "/" in result:
                result = result.split("/")[0]

    return result


def save_director(db, Director, film_html, film_information_id):
    """
    保存电影信息中的导演
    :return:
    """
    director_name_list = []
    directors_name = get_text_by_info(get_info(process_html(film_html)), "导演")
    if director_name_list is not None:
        director_name_list = directors_name.split("/")
    for director_name in director_name_list:
        if director_name is not None:
            director = Director(
                name=director_name,
                film_information_id=film_information_id
            )
            director_in_mysql_list = Director.query.filter(
                and_(Director.name == director.name,
                     Director.film_information_id == director.film_information_id)).all()
            if len(director_in_mysql_list) <= 0:
                db.session.add(director)
    db.session.commit()


def save_performer(db, Performer, film_html, film_information_id):
    """
    保存电影信息中的演员
    :return:
    """
    performer_name_list = []
    performers_name = get_text_by_info(get_info(process_html(film_html)), "主演")
    if performer_name_list is not None:
        performer_name_list = performers_name.split("/")
    for performer_name in performer_name_list:
        if performer_name is not None:
            performer = Performer(
                name=performer_name,
                film_information_id=film_information_id
            )
            performer_in_mysql_list = Performer.query.filter(
                and_(Performer.name == performer.name,
                     Performer.film_information_id == performer.film_information_id)).all()
            if len(performer_in_mysql_list) <= 0:
                db.session.add(performer)
    db.session.commit()


def save_film_type(db, FilmType, film_html, film_information_id):
    """
    保存电影信息中的类型
    :return:
    """
    film_type_name_list = []
    film_types_name = get_text_by_info(get_info(process_html(film_html)), "类型")
    if film_type_name_list is not None:
        film_type_name_list = film_types_name.split("/")
    for film_type_name in film_type_name_list:
        if film_type_name is not None:
            film_type = FilmType(
                name=film_type_name,
                film_information_id=film_information_id
            )
            film_type_in_mysql_list = film_type.query.filter(
                and_(FilmType.name == film_type.name,
                     FilmType.film_information_id == film_type.film_information_id)).all()
            if len(film_type_in_mysql_list) <= 0:
                db.session.add(film_type)
    db.session.commit()


def process_html(html):
    """
    处理html
    :return:
    """
    return BeautifulSoup(html, 'lxml')


def pull_film(db, Film, FilmInformation, Director, Performer, FilmType):
    """
    拉取分页下的电影
    :return:
    """
    # 从mysql获取最新not_pull的电影的id, 从这里开始拉取
    start_num = 0
    num = 0
    not_pull_film_list = Film.query.filter(Film.status == film_status.get("not_pull")).order_by(Film.id).limit(1).all()
    if len(not_pull_film_list) >= 1:
        num = math.floor(not_pull_film_list[0].id / 20) - 1
    else:
        pull_film_list = Film.query.filter(Film.status == film_status.get("pull")).order_by(Film.id).limit(1).all()
        if len(pull_film_list) >= 1:
            num = math.floor(not_pull_film_list[0].id / 20) - 1
    if num > 0:
        start_num = num * 20

    success = False
    retry_num = 3
    while True:
        try:
            success = real_pull(db, Film, FilmInformation, Director, Performer, FilmType, start_num)
        except Exception:
            time.sleep(10)
            try:
                real_pull(db, Film, FilmInformation, Director, Performer, FilmType, start_num)
            except Exception:
                time.sleep(20)
                real_pull(db, Film, FilmInformation, Director, Performer, FilmType, start_num)
        if success:
            start_num += 20
            retry_num = 3
        # 请求没有数据时重试3次
        else:
            time.sleep(5)
            retry_num -= 1
            if retry_num <= 0:
                start_num += 20
                retry_num = 3


def real_pull(db, Film, FilmInformation, Director, Performer, FilmType, start_num):
    """
    拉取分页下的电影
    :return:
    """
    # 请求API分类电影
    print("start_num = " + str(start_num))
    film_json_list = request_film(start_num)
    need_pull_film_information_url_list = []
    if film_json_list is not None:
        film_jsons = film_json_list.get("data")
        if film_jsons is not None:
            for film_json in film_jsons:
                need_pull_film_information_url_list.append(save_film(db, Film, film_json))
            time.sleep(5)
        else:
            return False
    else:
        return False
    # 拉取电影信息
    for subject_id, url in filter(lambda item: item is not None, need_pull_film_information_url_list):
        film_html = request_film_information(url)
        film_information_id = save_film_information(db, subject_id, FilmInformation, film_html)
        if film_information_id is not None:
            save_director(db, Director, film_html, film_information_id)
            save_performer(db, Performer, film_html, film_information_id)
            save_film_type(db, FilmType, film_html, film_information_id)
        Film.query.filter(Film.subject_id == subject_id).update({"status": film_status.get("pull")})
        time.sleep(5)
    return True


def is_number(s):
    try:
        # 如果能运行float(s)语句，返回True（字符串s是浮点数）
        float(s)
        return True
    except ValueError:
        pass
    try:
        # 把一个表示数字的字符串转换为浮点数返回的函数
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False
