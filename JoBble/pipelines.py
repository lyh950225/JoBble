# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import JsonItemExporter
import MySQLdb.cursors
from twisted.enterprise import adbapi
import MySQLdb


class JobblePipeline(object):
    def process_item(self, item, spider):
        return item


class JsonExportPipeline(object):
    #调用SCRAPY提供的Jsonexport 导出JSON文件
    def __init__(self):
        self.file = open('articleexport.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class MysqlTwistedPipline(object):
    # TWISTED异步插入MYSQL，只需要修改do_insert后面的逻辑即可重用
    # 根据不同的ITEM，构建不同的SQL语句并插入到MYDQL中
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
           host=settings["MYSQL_HOST"],
           db=settings["MYSQL_DBNAME"],
           user=settings["MYSQL_USER"],
           passwd=settings["MYSQL_PASSWORD"],
           charset='utf8',
           cursorclass=MySQLdb.cursors.DictCursor,
           use_unicode=True
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用TWISTED将MYSQL插入异步执行
        query = self.dbpool.runinteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)  # 处理异常

    def handle_error(self, failure, item, spider):
        # 处理异步插入异常
        print(failure)

    def do_insert(self, cursor, item):
        insert_sql, params = item.get_insert_sql()
        cursor.execute(insert_sql, params)
