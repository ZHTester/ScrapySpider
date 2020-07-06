# -*- coding: utf-8 -*-

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join, Identity
from w3lib.html import remove_tags
from LagouSpider.settings import SQL_DATETIME_FORMAT, SQL_DATE_FORMAT
import datetime
import re
import time

def remove_splash(value):
    """
    去掉工作城市的斜杠
    :param value:
    :return:
    """
    if '/' in value:
        return value.replace('/','')

def handle_jobaddr(value):
    # 
    addr_list = value.split('\n')
    addr_list = [ item.strip() for item in addr_list if item.strip() !="查看地图"]
    return ' '.join(addr_list)

def remove_all(value):
    # 删除对应的'\r\n'
    if '\r\n' in value:
        a = value.replace('\r\n','')
    
    if '\t' in a:
        b = a.replace('\t','')
        
    if '\xa0' in b:
        c =b.replace('\xa0','')
    
    if ' ' in c:
        d =c.replace(' ','')
    
    return d
     
def remove_title(value):
        if '\r\n\t\t\t\t\t\t' in value:
            return value.replace('\r\n\t\t\t\t\t\t','')
        
def replace_img(value):
    if 'full' in value:
        return value.replace('full','picture')
      
def remove_n(value):
    if '\n' in value:
        return value.replace('\n','')
class LagouItemLoader(ItemLoader):
    """
    拉钩网ITemLoader
    """
    default_output_processor = TakeFirst()
      
class LagouJobItem(scrapy.Item):
    """
    拉钩网职位招聘
    """
    title = scrapy.Field()
    url = scrapy.Field()
    url_object_id= scrapy.Field()
    salary = scrapy.Field()
    job_city =scrapy.Field(
        input_processor = MapCompose(remove_splash),
    )
    work_years=scrapy.Field(
        input_processor=MapCompose(remove_splash),
    )
    degree_need=scrapy.Field(
        input_processor = MapCompose(remove_splash),
    )
    job_type=scrapy.Field()
    publish_time=scrapy.Field(
        input_processor = MapCompose(remove_splash),
    )
    tags=scrapy.Field(
        input_processor= Join(','),
    )
    job_advantage=scrapy.Field()
    job_desc=scrapy.Field()
    job_addr=scrapy.Field(
        input_processor=MapCompose(remove_tags,handle_jobaddr),
    )
    company_name=scrapy.Field()
    crawl_time=scrapy.Field()
    crawl_update_time=scrapy.Field()


    def get_insert_sql(self):
        # 拉钩
        if 'https://passport.lagou.com' in self.get("url", ""):
            pass
        else:
            insert_sql = """
                insert into lagou_job(title, url, url_object_id, salary, job_city, work_years, degree_need,
                job_type, publish_time, tags, job_advantage, job_desc, job_addr, company_name,
                crawl_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE salary=VALUES(salary), job_desc=VALUES(job_desc)
            """
            params = (
                self.get("title", ""),
                self.get("url", ""),
                self.get("url_object_id", ""),
                self.get("salary", ""),
                self.get("job_city", ""),
                self.get("work_years", ""),
                self.get("degree_need", ""),
                self.get("job_type", ""),
                self.get("publish_time", ""),
                self.get("tags", ""),
                self.get("job_advantage", ""),
                self.get("job_desc", ""),
                self.get("job_addr", ""),
                self.get("company_name", ""),
                self["crawl_time"].strftime(SQL_DATETIME_FORMAT),
            )
            return insert_sql, params

class GoodShoesItemLoader(ItemLoader):
    """
    马甲网站好鞋ItemLoader
    """
    default_output_processor = TakeFirst()

class GoodShoesItem(scrapy.Item):
    """
    马甲网站数据抓取好鞋
    """
    title = scrapy.Field(
        input_processor=MapCompose(),
    )  # 商品名称
    url = scrapy.Field()  # 购买连接
    price = scrapy.Field()  # 购买价格
    information = scrapy.Field(
        input_processor =  MapCompose(remove_n),
        )  # 商品标签
    Introduction = scrapy.Field()  # 商品简介
    img_path = scrapy.Field()  # 商品存储路径
    img_url = scrapy.Field(
        output_processor=Identity(),  # 保持原样的url
    )  # 商品图片地址
    fid = scrapy.Field()  # 0
    pid = scrapy.Field()  # 1
    ty = scrapy.Field()  # 3
    tty = scrapy.Field()  # 0
    ttty = scrapy.Field()  # 0
    pricetitles = scrapy.Field()
    # status
    statuss = scrapy.Field()
    sendtime = scrapy.Field()

    def get_insert_sql(self):
        # 插入数据库
        insert_sql = """
            insert into jd_sport(title, introduce, price,img1, linkurl, content,fid,pid,ty,tty,ttty,pricetitle,status,sendtime) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
            ON DUPLICATE KEY UPDATE price=VALUES(price)
        """
        params = (
            self.get("title", ""),
            self.get("information", ""),
            self.get("price", ""),
            self.get("img_url", ""),
            self.get("url", ""),
            self.get("Introduction", ""),
            self.get("fid", "0"),
            self.get("pid", "1"),
            self.get("ty", "3"),
            self.get("tty", "0"),
            self.get("ttty", "0"),
            self.get("pricetitles", "¥"),
            self.get('statuss', '1'),
            self.get('sendtime', '')

        )
        return insert_sql, params

class YougouItemLoader(ItemLoader):
    """
    马甲网站ItemLoader
    """
    default_output_processor = TakeFirst()

class YougouItem(scrapy.Item):
    # 马甲网站数据抓取优个网
    title =  scrapy.Field(
        input_processor =  MapCompose(remove_title),
        )  # 商品名称
    category =  scrapy.Field()
    url  =  scrapy.Field()  # 购买连接
    price = scrapy.Field()  # 购买价格
    information = scrapy.Field()  # 商品标签
    Introduction = scrapy.Field(
       input_processor =  MapCompose(remove_all),
        )  # 商品简介
    img_path= scrapy.Field()  # 商品存储路径
    img_url= scrapy.Field(
        output_processor = Identity(),  # 保持原样的url
        )  # 商品图片地址
    fid = scrapy.Field() #0
    pid = scrapy.Field()  # 1
    ty = scrapy.Field()   # 3
    tty = scrapy.Field()  # 0
    ttty = scrapy.Field()  # 0
    pricetitles = scrapy.Field()
    # status  
    statuss = scrapy.Field()
    sendtime = scrapy.Field()
    
    
    def get_insert_sql(self):
        # 插入数据库
        insert_sql = """
            insert into jd_sport(title, introduce, price,img1, linkurl, content,fid,pid,ty,tty,ttty,pricetitle,status,sendtime) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
            ON DUPLICATE KEY UPDATE price=VALUES(price)
        """
        params = (
            self.get("title", ""),
            self.get("information", ""),
            self.get("price", ""),
            self.get("img_url", ""),
            self.get("url", ""),
            self.get("Introduction", ""),
            self.get("fid", "0"),
            self.get("pid", "1"),
            self.get("ty", "3"),
            self.get("tty", "0"),
            self.get("ttty", "0"),
            self.get("pricetitles", "¥"),
            self.get('statuss','1'),
            
            self.get('sendtime','')
            
        )
        return insert_sql, params
    
