# -*- coding: utf-8 -*-
import re
import logging
import scrapy
from scrapy_redis.spiders import RedisSpider
from redis import Redis
from time import sleep
from bs4 import BeautifulSoup
from ..items import NextUrlsItem
from .logic import *

logger = logging.getLogger('spridermas')

class RedisSpider(RedisSpider):
    #主爬虫功能 
    # 1、爬取下一页地址，放到urls_request待继续爬取 
    # 2、每个爬取页面中取出待爬网址，放到urls_slaver供给子爬虫爬取
    # 3、已爬取成功的地址，放到放url_filter用于过滤
    name = 'spridermas' 
    redis_key = 'mysprider:urls_request'
    #allowed_domains = [] 

    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.allowed_domans = filter(None, domain.split(','))
        super(RedisSpider, self).__init__(*args, **kwargs)


    def parse(self, response):
        item = NextUrlsItem()
        redis = Redis()

        try:
            if msdytt.homeurl in response.url:
                m = msdytt.logicDytt()
                m.parseMas(redis, response)
            elif msdymf.homeurl in response.url:
                m = msdymf.logicDymf()
                m.parseMas(redis, response)
            sleep(0.25)
            logger.info('crawling ' + response.url)
        except Exception as e:
            logger.error(e)
            
        yield item