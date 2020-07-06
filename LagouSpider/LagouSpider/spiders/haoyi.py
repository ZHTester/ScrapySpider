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



class HaoyiSpider(CrawlSpider):
    name = 'haoyi'
    allowed_domains = ['www.dku51.com']
    start_urls = ['http://www.dku51.com/']

    rules = (
        Rule(LinkExtractor(allow=r'goods-\d+.html'), callback='parse_item', follow=True),
    )
    def parse_item(self, response):
        # 好衣服抓取 
        item_loader = GoodShoesItemLoader(item=GoodShoesItem(), response=response)
        # item_loader.add_xpath('title', '//*[@class="summary"]/h2/text()')
        item_loader.add_css('title', '.summary h2::text')
        item_loader.add_xpath('Introduction','//*[@class="salebox"]/p[2]/b/span/span/text()')  # 简介
        item_loader.add_xpath('Introduction','//*[@class="saledesc"]/span/strong/text()')
        item_loader.add_xpath('information','//*[@class="summary"]/ul/li[1]/text()')  # 标签
        item_loader.add_value('url', response.url)
        # 下载图片
        img_urlss = response.xpath( '//*[@id="goodsPhotoList"]/li/a/img/@src').extract()
        item_loader.add_value('img_url',img_urlss)
        # 价格
        item_loader.add_xpath('price','//*[@class="summary"]/ul/li[2]/b/span/text()')
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

        goods_haoyi = item_loader.load_item()
        return goods_haoyi
