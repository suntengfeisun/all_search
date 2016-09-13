# -*- coding: utf-8 -*-


import time


class Config:
    mysql_host = "112.124.50.167"
    mysql_user = "root"
    mysql_password = 'kongquewangchao'
    mysql_dbname = "allsearch"
    mysql_port = 3306
    mysql_charset = 'utf8'
    # mysql重试次数
    mysql_retry_times = 5
    # mysql 连接池 最大 连接数
    mysql_max_cached = 10

    #url_main = 'http://www.ygdy8.net'
    sleep_time = 3600
    headers_path = '/mnt/crawler/allsearch/crawler/'
    headers_referer = 'http://www.baidu.net/'

    time_now = time.strftime('%Y-%m-%d %H:%M:%S')
