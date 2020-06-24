# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
import pymysql
import pymysql.cursors

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
from twisted.enterprise import adbapi

class ArticlespiderPipeline:
    def process_item(self, item, spider):
        return item

#自定义将数据存入mysql
class MysqlPipeline(object):
    #使用同步机制插入数据库
    def __init__(self):
        self.conn = pymysql.connect("192.168.25.132", "root", "root", "pythonpro", charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            insert into jobbole_article(title, url, create_date)
            values (%s, %s, %s)
        """
        self.cursor.execute(insert_sql, (item["title"], item["url"], item["create_date"]))
        self.conn.commit()


class MysqlTwistedPipline(object):
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
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("pymysql", **dbparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        #使用twisted将MySQL插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error)#处理异常

    def handle_error(self, failure, item, spider):
        #处理异步插入的异常
        print(failure)


    def do_insert(self, cursor, item):
        #执行具体的插入
        insert_sql = """
                    insert into jobbole_article(title, url, create_date)
                    values (%s, %s, %s)
                """
        cursor.execute(insert_sql, (item["title"], item["url"], item["create_date"]))

#将爬取的结果保存为json文件，自定义json文件的导出
class JsonWithEncodingPipeline(object):
    def __init__(self):
        self.file = codecs.open('article.json', 'w', encoding="utf-8")
    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item
    def spider_closed(self, spider):
        self.file.close()


class JsonExporterPipeline(object):
    #调用scrapy提供的json export 导出json文件
    def __init__(self):
        self.file = open('articleexport.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding = "utf-8", ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        for ok, value in results:
            image_file_path = value["path"]
        item["front_image_path"] = image_file_path

        return item