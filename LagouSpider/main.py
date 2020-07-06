# encoding: utf-8

"""
# @Time    : 31/3/2020 2:26 下午
# @Author  : Function
# @FileName    : main.py
# @Software: PyCharm
"""
from scrapy.cmdline import execute
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# execute(['scrapy','crawl','haoyi'])
# execute(['scrapy','crawl','jd'])
execute(['scrapy','crawl','jd'])
