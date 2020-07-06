# -*- coding: utf-8 -*-
import scrapy
import os
import sys
base_path = os.getcwd()  # 获取当前路径
sys.path.append(base_path)  # 加入到当前路径中 
import random
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import YougouItem,YougouItemLoader
import time 

class JdSpider(CrawlSpider):
    name = 'jd'
    # allowed_domains = ['pindao.suning.com']
    start_urls = ['http://www.yoger.com.cn/']

    rules = (
        Rule(LinkExtractor(allow=r'product/\d+.html'), callback='parse_jd_sport', follow=True),
    )

    def parse_jd_sport(self, response):
        # 解析优个网
        # 回掉函数
        item_loader = YougouItemLoader(item=YougouItem(), response=response)
        item_loader.add_css('title', '.xq_xinxi h1::text')
        item_loader.add_value('url', response.url)
        item_loader.add_xpath('information','//*[@class="mbx"]/a[3]/text()')
        item_loader.add_xpath('Introduction','//*[@class="pp_js"]/p/text()')
        item_loader.add_xpath('category','//*[@class="mbx"]/a[2]/text()')
        # 下载图片
        img_urlss = response.css( '.chanpin_datu img::attr(src)').extract()  
        item_loader.add_value('img_url',img_urlss)
        # 价格
        pirce_random = random.randint(50,800) # 随机生成价格
        item_loader.add_value('price',pirce_random)
        # 对应ID
        item_loader.add_value('fid',"0")
        item_loader.add_value('pid',"1")
        item_loader.add_value('ty',"3")
        item_loader.add_value('tty',"0")
        item_loader.add_value('ttty',"0")
        item_loader.add_value('pricetitles','元')
        send_time = time.time()
        item_loader.add_value('sendtime',send_time)
        item_loader.add_value('statuss','1')
        yougou = item_loader.load_item()
        
        
        return yougou
