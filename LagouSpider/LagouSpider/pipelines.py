# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
import sys
base_path = os.getcwd()  # 获取当前路径
sys.path.append(base_path)  # 加入到当前路径中 
from scrapy.pipelines.images import ImagesPipeline
from pymysql.cursors import DictCursor
from twisted.enterprise import adbapi   # 异步提交api库


class MajiaImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        """
         ---马甲网图片过滤---
        """
        img_path = ''
        if 'img_url' in item:
            for ok,value in results:
                img_path = value['path']
            if 'full' in img_path:
                img_path = img_path.replace('full','picture/full')
                item['img_url'] = img_path
            else:
                item['img_url'] = img_path
        return  item
    
    
class LagouspiderPipeline(object):
    def process_item(self, item, spider):
        if '包'  in item['category']:
            item['ty'] = '6'
        elif '球' in item['category']:
            item['ty'] = '4'
        elif '衣' or '服' or '裤' in item['category']:
            item['ty'] = '5'
        elif '球鞋' in item['category']:
            item['ty'] = '7'
        else:
            item['ty'] = '3'
            
        return item

class MysqlTwistedPipline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        """
        自动添加内部的方法
        自动传递内部方法
        :param settings:
        :return:
        """
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=DictCursor,
            use_unicode=True,
        )

        dbpool = adbapi.ConnectionPool('pymysql', **dbparms)  # 创建连接
        return cls(dbpool)  # 自动注入返回

    def process_item(self, item, spider):
        # 使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)  # 处理异常
        return item

    def handle_error(self, failure, item, spider):
        # 处理异步插入的异常
        print(failure)

    def do_insert(self, cursor, item):
        # 执行具体的插入
        # 根据不同的item 构建不同的sql语句并插入到mysql中
        insert_sql, params = item.get_insert_sql()
        # print("-------this is me------------------{0}------------------------------".format(params))
        cursor.execute(insert_sql, params)
