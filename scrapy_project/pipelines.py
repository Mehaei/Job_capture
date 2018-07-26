# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.conf import settings
import pymysql

class ScrapyProjectPipeline(object):
    def process_item(self, item, spider):
        return item

class MysqlPipeline(object):
    def open_spider(self,spider):
        my = settings['MYSQL']
        # print(my)
        self.db = pymysql.connect(my['host'],my['user'],my['password'],my['db'],charset="utf8")
        self.cursor = self.db.cursor()

    def process_item(self,item,spider):
        sql,data = item.get_sql()
        try:
            self.cursor.execute(sql,data)
            self.db.commit()
        except Exception as e:
            print('写入数据库错误',e)
            self.db.rollback()
        return item
    def close_spider(self,spider):
        self.cursor.close()
        self.db.cursor()