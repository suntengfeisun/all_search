# -*- coding: utf-8 -*-


import MySQLdb
from DBUtils.PooledDB import PooledDB
from config import Config
from time import sleep
import sys


class MysqlDao():
    def __init__(self):
        self._init_mysql()

    def _init_mysql(self):
        n = 0
        while True:
            try:
                pool = PooledDB(MySQLdb, Config.mysql_max_cached, host=Config.mysql_host, user=Config.mysql_user,
                                passwd=Config.mysql_password, db=Config.mysql_dbname, port=Config.mysql_port,
                                charset=Config.mysql_charset)
                self._conn = pool.connection()
                break
            except Exception, e:
                print Exception, ":", e
                if n >= Config.mysql_retry_times:
                    print ('Mysql Connect Error,exit!')
                    sys.exit()
                else:
                    n = n + 1
                    print ('Mysql Connect Error,sleep!')
                    sleep(100)

    def execute(self, sql):
        cur = self._conn.cursor()
        cur.execute(sql)
        res = cur.fetchall()
        self._conn.commit()
        cur.close()
        return res

    def executeValues(self, sql, values):
        cur = self._conn.cursor()
        cur.execute(sql, values)
        res = cur.fetchall()
        self._conn.commit()
        cur.close()
        return res

    def close(self):
        self._conn.close()
