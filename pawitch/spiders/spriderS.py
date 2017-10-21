# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisSpider
import scrapy
import re
from redis import Redis
from time import sleep
from bs4 import BeautifulSoup
from ..items import MovieItem
from .tools import *
from .logic import *

class RedisSpider(RedisSpider):
    #子爬虫功能 
    # 取主机redis中urls_slaver地址爬取
    name = 'spridersla' 
    redis_key = 'mysprider:urls_slaver'

    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.allowed_domans = filter(None, domain.split(','))
        super(RedisSpider, self).__init__(*args, **kwargs)


    def parse(self, response):
        redis = Redis()
        item = MovieItem()
        #如果url未被爬过，则执行
        if redis.sismember('mysprider:urls_filter', response.url) == 0:
            #爬取页面内容
            if msdytt.homeurl in response.url:
                web1 = msdytt.logicDytt()
                web1.parseSla(redis, response)
            elif msdymf.homeurl in response.url:
                web2 = msdymf.logicDymf()
                web2.parseSla(redis, response)
            #sleep(0.25)
            print('--------crawling-------- ' + response.url)
        else:
            print('--------already complete--------')

        yield item