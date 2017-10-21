# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisSpider
import scrapy
import re
import logging
from redis import Redis
from time import sleep
from bs4 import BeautifulSoup
from ..items import MovieItem
from .tools import tmysql
from .tools import turl

class RedisSpider(RedisSpider):
    #子爬虫功能 
    # 取主机redis中urls_slaver地址爬取
    name = 'spridersla' 
    redis_key = 'mysprider:urls_slaver'

    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.allowed_domans = filter(None, domain.split(','))
        super(RedisSpider, self).__init__(*args, **kwargs)


    def replace_chara(markup):
        return markup.replace(u'\xa0' , u' ')

    '''
    def saveToFile(soup, name):
        fp = open('D:/name.txt', "wb+")
        # 1
        filminfo = soup.findall('p')
        for info in filminfo:
                #print(info.get_text("|", strip=True).replace(u'\xa0' , u' '))

                item['download'] = info.get_text("|", strip=True).replace(u'\xa0' , u' ')
                
                fp.write(bytes(item['download'].encode('utf-8', 'ignore'))) 
                fp.write('\r\n'.encode())
        fp.close()

        # 2
        filminfo = soup.find('div', id = 'Zoom').stripped_strings
        for info in filminfo:
            print(repr(info))
            fp.write(bytes(repr(info).encode('utf-8', 'ignore'))) 

        # 3
        # xpath 查出div，id是Zoom的
        # for info in response.xpath('//div[@id="Zoom"]'):
        #     item['introduce'] = info.xpath('p').extract()
        #     print(item['introduce'])
        #     if info.xpath('a/@href').extract() != []:
        #         item['download'] = info.xpath('a/@href').extract()
        #         #print(item['download'])
                
        #         #爬取成功存到已爬取
        #         r.sadd('mysprider:urls_filter', response.url)
    '''

    def parseSPartOne(self, redis, response):
        soup = BeautifulSoup(response.body.decode('gb2312', 'ignore'), 'lxml')
    
        #saveToFile(soup)

        #取迅雷地址
        #怎么取jason中的数据？？
        url = soup.find('td', style="WORD-WRAP: break-word").get_text()
        name = soup.find('title').get_text()
        # print(soup.find('td', style="WORD-WRAP: break-word"))
        # print(soup.find('title'))

        db = tmysql.Mysql()
        #sql = 'insert into filminfo(fid, name, download, introduce) values (1,"22222","")'
        attrs = ['name', 'download', 'introduce']
        value = [str(name), str(url), '']
        db._insert('filminfo', attrs, value)
        
        #re.compile('thunder:.*=')
        #爬取成功存到已爬取
        redis.sadd('mysprider:urls_filter', response.url)

    def parseSPartTwo(self, redis, response):
        db = tmysql.Mysql()
        attrs = ['name', 'direct', 'actor', 'introduce', 'score', 'date', 'status', 'udownload', 'upassword', 'uonline', 'uonlineshort', 'uindex'] 
            
        status = 0
        udownload = ''
        upassword = ''
        uonline = ''
        uonlienshort = ''

        soup = BeautifulSoup(response.body.decode('utf-8', 'ignore'), 'lxml')
        textInfo = soup.find('div', class_ = 'movie-meta')  
        fname = textInfo.find('h1').get_text()
        filmInfo = textInfo.find_all('p')
        fdirect = filmInfo[0].get_text()
        factor = filmInfo[2].get_text()
        ftype = filmInfo[3].get_text()
        ftime = filmInfo[6].get_text()
        fscore = filmInfo[9].get_text()
        fintroduce = soup.find('div', class_ = 'movie-introduce').get_text()

        #uonline = soup.find('iframe', attrs={'name': 'tv'})
        frame = soup.find('iframe')
        if frame is not None: 
            uonline = frame.get('src')
            if uonline.startswith('/'):
                uonline = 'http://www.dybee.cn' + uonline
            uonlienshort = turl.urlToShort(uonline)
        else:
            uonline = ''

        urls = soup.find('table', class_ = 'table table-hover')
        if urls is not None:
            for url in urls.find_all('a'):
                udownload = url.get('href') #暂时只留最后一个链接,需要处理对应密码，如果有多个网盘可妥了，密码错乱，一直是最后一个
                if udownload.startswith('https://pan.baidu.com'):
                    upassword = urls.find('strong').get_text()
                else:
                    upassword = ''
        else:
            if udownload == '':
                status = 1

        value = [fname, fdirect, factor, fintroduce, fscore, str(ftime), str(status), udownload, upassword, uonline, uonlienshort, response.url]
        db._insert('filminfo', attrs, value)

        redis.sadd('mysprider:urls_filter', response.url)


    def parse(self, response):
        redis = Redis()
        item = MovieItem()
        #如果url未被爬过，则执行
        if redis.sismember('mysprider:urls_filter', response.url) == 0:
            #爬取页面内容
            #parseSPartOne(redis, response)
            self.parseSPartTwo(redis, response)
        else:
            print('------------already complete')

        yield item