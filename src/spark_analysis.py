# -*- coding: UTF-8 -*-

import json

import pymysql
from pyspark import SparkConf, SparkContext

"""
Spark版本: 3.2.1
执行命令:
spark-submit \
--master spark \
--driver-memory 1g \
--num-executors 2 \
--executor-memory 1g \
--executor-cores 1 \
--conf spark.pyspark.python=/usr/bin/python3 \
./spark_analysis.py
"""

# spark上下文
conf = SparkConf().setMaster("local").setAppName("douban_film_analysis")
sc = SparkContext(conf=conf)

# mysql连接
db = pymysql.connect(host='192.168.0.103', user='root', password='123456', port=3306, db='douban_film_analysis')
cursor = db.cursor()


def write_file(file_name, result):
    """
    将计算结果写入json文件
    :return:
    """
    with open(file_name, "w") as fp:
        json.dump(result, fp, ensure_ascii=False, indent=4)


def language_calculate():
    """
    语言统计
    :return:
    """
    cursor.execute("SELECT language FROM t_film_information")
    rdd = sc.parallelize(cursor.fetchall())
    language_count_dict = rdd.map(lambda x: x[0]).countByValue()
    top_10_list = sorted(language_count_dict.items(), key=lambda x: x[1], reverse=True)
    result = list(map(lambda x: {
        "name": x[0],
        "total": x[1]
    }, top_10_list[:10]))

    write_file("language_top_10.json", result[:10])


def score_film_length_calculate():
    """
    评分-时长计算
    :return:
    """
    cursor.execute("SELECT film_length, score FROM t_film_information")
    rdd = sc.parallelize(cursor.fetchall())
    filter_rdd = rdd.filter(lambda x: x is not None) \
        .filter(lambda x: x[0] is not None) \
        .filter(lambda x: x[0] != "null") \
        .filter(lambda x: x[0] != "NULL") \
        .filter(lambda x: x[0] != "Null") \
        .filter(lambda x: x[0] != "") \
        .filter(lambda x: x[0] != " ")
    score_length = filter_rdd.map(lambda x: (int(x[0]), x[1])) \
        .sortBy(lambda x: x[0], ascending=False) \
        .map(lambda x: {"length": x[0], "score": x[1]}) \
        .collect()
    write_file("score_length.json", score_length)


def director_calculate():
    """
    导演电影数量Top n
    :return:
    """
    cursor.execute("SELECT name FROM t_director")
    rdd = sc.parallelize(cursor.fetchall())
    director_count_dict = rdd.map(lambda x: x[0]).countByValue()
    top_10_list = sorted(director_count_dict.items(), key=lambda x: x[1], reverse=True)
    result = list(map(lambda x: {
        "name": x[0],
        "total": x[1]
    }, top_10_list[:10]))

    write_file("director_top_10.json", result)


def film_type_calculate():
    """
    电影类型
    :return:
    """
    cursor.execute("SELECT name FROM t_film_type")
    rdd = sc.parallelize(cursor.fetchall())
    film_type_count_dict = rdd.map(lambda x: x[0]).countByValue()
    result = []
    for film_type, value in film_type_count_dict.items():
        result.append({
            "name": film_type,
            "value": value
        })

    write_file("film_type.json", result)


def country_or_region_calculate():
    """
    各国电影计数
    :return:
    """
    cursor.execute("SELECT country_or_region FROM t_film_information")
    rdd = sc.parallelize(cursor.fetchall())
    country_count_dict = rdd.map(lambda x: x[0]).countByValue()
    result = []
    for count_or_region, total in country_count_dict.items():
        result.append({
            "name": count_or_region,
            "total": total
        })

    write_file("country_or_region_count.json", result)


def get_statistics():
    """
    全局统计数据
    :return:
    """
    cursor.execute("SELECT subject_id FROM t_film_information")
    film_information_total = sc.parallelize(cursor.fetchall()).distinct().count()

    cursor.execute("SELECT name FROM t_director")
    director_total = sc.parallelize(cursor.fetchall()).distinct().count()

    cursor.execute("SELECT name FROM t_performer")
    performer_total = sc.parallelize(cursor.fetchall()).distinct().count()

    cursor.execute("SELECT name FROM t_film_type")
    film_type_total = sc.parallelize(cursor.fetchall()).distinct().count()

    cursor.execute("SELECT country_or_region FROM t_film_information")
    country_or_region_total = sc.parallelize(cursor.fetchall()).distinct().count()

    write_file("statistics.json",
               {
                   "film_total": film_information_total,
                   "country_total": country_or_region_total,
                   "film_type_total": film_type_total,
                   "director_total": director_total,
                   "performer_total": performer_total
               })


if __name__ == '__main__':
    language_calculate()
    score_film_length_calculate()
    director_calculate()
    film_type_calculate()
    country_or_region_calculate()
    get_statistics()
