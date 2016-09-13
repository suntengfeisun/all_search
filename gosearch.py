# -*- coding: utf-8 -*-

import sys
import threading
import requests
from lxml import etree
from mysqlpooldao import MysqlDao
import time
from headers import Headers
import simplejson
from config import Config

reload(sys)
sys.setdefaultencoding('utf8')


class Worker(threading.Thread):
    def baidu(self, word):
        ret = []
        url = 'http://m.baidu.com/s?word=' + word
        headers = Headers.getHeaders()
        req = requests.get(url, headers=headers, timeout=30)
        if req.status_code == 200:
            html = req.content
            selector = etree.HTML(html)
            words = selector.xpath('//div[@class="rw-list"]/a/text()')
            ret.extend(words)
        print('baidu', ret)
        return ret

    def sogou(self, word):
        ret = []
        headers = Headers.getHeaders()
        headers['Referer'] = 'https://www.sogou.com/'
        url = 'http://m.sogou.com/web/searchList.jsp?pg=webSearchList&v=2&keyword=' + word
        req = requests.get(url, headers=headers, timeout=30)
        if req.status_code == 200:
            html = req.content
            selector = etree.HTML(html)
            words = selector.xpath('//div[@class="bc relate"]/a/text()')
            ret.extend(words)
        print('sogou', ret)
        return ret

    def so(self, word):
        ret = []
        headers = Headers.getHeaders()
        headers['Referer'] = 'https://www.so.com/'
        url = 'http://www.so.com/s?q=' + word
        req = requests.get(url, headers=headers, timeout=30)
        if req.status_code == 200:
            html = req.content
            selector = etree.HTML(html)
            words = selector.xpath('//div[@id="rs"]/table/tr/th/a/text()')
            ret.extend(words)
        print('so', ret)
        return ret

    def bing(self, word):
        ret = []
        headers = Headers.getHeaders()
        url = 'http://global.bing.com/search?q=' + word
        req = requests.get(url, headers=headers, timeout=30)
        if req.status_code == 200:
            html = req.content
            selector = etree.HTML(html)
            words = selector.xpath('//li[@class="b_ans"]/ul/li/a/descendant::text()')
            ret.extend(words)
        return ret

    def getSearch(self, word):
        all_search = []
        baidu = self.baidu(word)
        sogou = self.sogou(word)
        so = self.so(word)
        # bing = self.bing(word)
        all_search.extend(baidu)
        all_search.extend(sogou)
        all_search.extend(so)
        print(all_search)
        return all_search

    def run(self):
        mysqlDao = MysqlDao()
        while True:
            print(self.name)
            sql = 'select * from allsearch_key_word WHERE `status`=0 limit 0,1'
            ret = mysqlDao.execute(sql)
            if (len(ret) > 0):
                res = ret[0]
                id = res[0]
                sql = 'update allsearch_key_word set `status`=2 where `id`=' + str(id)
                mysqlDao.execute(sql)
                word = res[1]
                sql_values = self.getSearch(word)
                for sql_value in sql_values:
                    created_at = time.strftime('%Y-%m-%d %H:%M:%S')
                    values = (sql_value, id, 0, created_at)
                    sql = 'insert ignore into allsearch_key_word (`word`,`parent_id`,`status`,`created_at`) VALUES (%s,%s,%s,%s)'
                    mysqlDao.executeValues(sql, values)
                sql = 'update allsearch_key_word set `status`=2 where `id`=' + str(id)
                mysqlDao.execute(sql)
            else:
                print(self.name + 'sleep')
                time.sleep(3600)
        mysqlDao.close()


if __name__ == '__main__':
    worker_num = 10
    threads = []
    for x in xrange(0, worker_num):
        threads.append(Worker())
    for t in threads:
        t.start()
        time.sleep(5)
    for t in threads:
        t.join()
