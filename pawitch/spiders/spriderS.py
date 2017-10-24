# -*- coding: utf-8 -*-
import re
import logging
import scrapy
from scrapy_redis.spiders import RedisSpider
from redis import Redis
from time import sleep
from bs4 import BeautifulSoup
from ..items import MovieItem
from .logic import *
from .tools import *

logger = logging.getLogger('spridersla')

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
        
        try:
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
                logger.info('crawling ' + response.url)
            else:
                logger.warning('already complete ' + response.url)
        except Exception as e:
            logger.error(e)

        yield item