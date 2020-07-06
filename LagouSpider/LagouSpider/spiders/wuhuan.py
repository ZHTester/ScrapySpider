# -*- coding: utf-8 -*-
import scrapy
import os
import sys
base_path = os.getcwd()  # 获取当前路径
sys.path.append(base_path)  # 加入到当前路径中 
import random
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import GoodShoesItem,GoodShoesItemLoader
import time


class WuhuanSpider(CrawlSpider):
    name = 'wuhuan'
    # allowed_domains = ['www.hiwuhuan.com']
    start_urls = ['https://www.hiwuhuan.com/']

    rules = (
        # Rule(LinkExtractor(allow=r'.*'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'product/\d+.html'), callback='parse_shose', follow=True),
    )

    def parse_shose(self, response):
        # 好鞋数据爬取  北京五环购物中心
        item_loader = GoodShoesItemLoader(item=GoodShoesItem(), response=response)
        item_loader.add_xpath('title','//*[@id="box"]/div[1]/div/div[2]/p[1]/text()')
        item_loader.add_xpath('Introduction','//*[@id="box"]/div[2]/div[2]/div/div[1]/p/text()')
        item_loader.add_xpath('information','//*[@id="box"]/div[1]/p/span/a[3]/text()')
        item_loader.add_value('url', response.url)
        # 下载图片
        img_urlss = response.xpath( '//*[@id="zoom1"]/@href').extract()
        item_loader.add_value('img_url',img_urlss)
        # 价格
        pirce_random = random.randint(50,800) # 随机生成价格
        item_loader.add_value('price',pirce_random)
        # 对应状态ID
        item_loader.add_value('fid',"0")
        item_loader.add_value('pid',"1")
        item_loader.add_value('ty',"5")
        item_loader.add_value('tty',"0")
        item_loader.add_value('ttty',"0")
        item_loader.add_value('pricetitles','元')
        send_time = time.time()
        item_loader.add_value('sendtime',send_time)
        item_loader.add_value('statuss','1')

        goods_shoes = item_loader.load_item()
        return goods_shoes