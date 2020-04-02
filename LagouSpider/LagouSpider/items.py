# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join, Identity
from w3lib.html import remove_tags
from LagouSpider.settings import SQL_DATETIME_FORMAT, SQL_DATE_FORMAT
import datetime
import re




class LagouItemLoader(ItemLoader):
    """
    拉钩网ITemLoader
    """
    default_output_processor = TakeFirst()


def remove_splash(value):
    """
    去掉工作城市的斜杠
    :param value:
    :return:
    """
    if '/' in value:
        return value.replace('/','')

def handle_jobaddr(value):
    addr_list = value.split('\n')
    addr_list = [ item.strip() for item in addr_list if item.strip() !="查看地图"]
    return ' '.join(addr_list)

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
