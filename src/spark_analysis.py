# -*- coding: UTF-8 -*-

from pyspark import SparkConf, SparkContext

if __name__ == '__main__':
    conf = SparkConf().setMaster("local").setAppName("douban")
    sc = SparkContext(conf=conf)
    rdd = sc.parallelize([1, 2, 3, 4])
    rdd.foreach(print)
