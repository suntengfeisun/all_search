# -*- coding: utf-8 -*-
'''
关键词搜索
'''
import sys
import time
import requests
from headers import Headers
from lxml import etree
from mysqlpooldao import MysqlDao

reload(sys)
sys.setdefaultencoding('utf8')

while True:
    try:
        url = 'http://top.baidu.com/'
        headers = Headers.getHeaders()
        req = requests.get(url, headers=headers, timeout=30)
        if req.status_code == 200:
            html = req.content.decode('gb2312', 'ignore')
            selector = etree.HTML(html)
            words = selector.xpath('//div[@id="box-cont"]/descendant::a/@title')
            for word in words:
                print(word)
                mysqlDao = MysqlDao()
                sql = 'insert ignore into allsearch_key_word (`word`,`parent_id`,`status`,`created_at`) VALUES (%s,%s,%s,%s)'
                created_at = time.strftime('%Y-%m-%d %H:%M:%S')
                values = (word, 0, 0, created_at)
                mysqlDao.executeValues(sql, values)
                mysqlDao.close()
        else:
            print('code error')
    except:
        pass
    time.sleep(21600)


