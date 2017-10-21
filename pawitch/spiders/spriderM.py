# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisSpider
import scrapy
from scrapy import log
from redis import Redis
from time import sleep
from bs4 import BeautifulSoup
import re
from ..items import NextUrlsItem

class RedisSpider(RedisSpider):
    #主爬虫功能 
    # 1、爬取下一页地址，放到urls_request待继续爬取 
    # 2、每个爬取页面中取出待爬网址，放到urls_slaver供给子爬虫爬取
    # 3、已爬取成功的地址，放到放url_filter用于过滤
    name = "spridermas" 
    redis_key = 'mysprider:urls_request'
    #allowed_domains = [] 
    

    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.allowed_domans = filter(None, domain.split(','))
        self.index_list = ('http://www.dytt8.net/', 'http://www.dybee.cn')
        super(RedisSpider, self).__init__(*args, **kwargs)

    def parseMPartOne(self, redis, response):
        print('爬取1------------' + self.index_list[0])
        # 页面跳转信息
        soup = BeautifulSoup(response.body.decode('gb2312', 'ignore'), 'lxml')
        for pageInfo in soup.find_all('div', class_='x'):
            pageUrl = re.findall(r'<a href="(.*?)">.*</a>', repr(pageInfo))
            if pageUrl != []:
                redis.lpush('mysprider:urls_request', self.index_list[0] + 'html/gndy/dyzz/' + pageUrl[-2])
                self.log(pageUrl, level=log.INFO)
                sleep(0.25)

        # 为什么不好使了？？？
        #for pageInfo in response.xpath('//div[@class="x"]'):
            # pageUrl = pageInfo.xpath('a/@href').extract()
            # if pageUrl != []:
            #     r.lpush('mysprider:urls_request', self.url + pageUrl[-2])
            #     self.log(pageUrl, level=log.INFO)
            #     sleep(0.5)
        # 当前页面待爬链接
        for urls in response.xpath('//b'):
            slaverurl = urls.xpath('a/@href').extract()
            if slaverurl != []:
                redis.rpush('mysprider:urls_slaver', self.index_list[0] + slaverurl[0])


    def parseMPartTwo(self, redis, response):
        print('爬取2------------' + self.index_list[1])
        soup = BeautifulSoup(response.body.decode('utf-8', 'ignore'), 'lxml')

        pageInfo = soup.find('a', class_ = 'next page-numbers')
        if pageInfo is not None:
            redis.lpush('mysprider:urls_request', self.index_list[1] + pageInfo.get('href'))
            sleep(0.25)
            
        for urls in soup.find_all('a', target = '_blank', class_ = re.compile('user_list_(.*?)')):
            if urls is not None:
                strs = self.index_list[1]
                if urls.get('href').startswith('http://www.dybee.cn'):
                    strs = urls.get('href')
                else:
                    strs += urls.get('href')
                redis.rpush('mysprider:urls_slaver', strs)

    def parse(self, response):
        item = NextUrlsItem()
        redis = Redis()

        #self.parseMPartOne(redis, response)
        self.parseMPartTwo(redis, response)

        yield item
        

                
