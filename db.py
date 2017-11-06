# encoding=utf-8

import pymysql
import arrow
import ujson
from settings import MYSQL_HOST, MYSQL_DB, MYSQL_USER, MYSQL_PASSWD


class DB:
    def __init__(self):
        self.connect = pymysql.connect(
            host=MYSQL_HOST,
            db=MYSQL_DB,
            user=MYSQL_USER,
            passwd=MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True
        )
        self.cursor = self.connect.cursor()

    def insert(self, item):
        sql, values = item.form_sql_values()
        try:
            self.curosr.execute(sql, values)
            self.connect.commit()
        except Exception as e:
            print(e)
