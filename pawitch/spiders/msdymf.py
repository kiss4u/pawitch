# -*- coding: utf-8 -*-
from time import sleep
from bs4 import BeautifulSoup
from .tools import tmysql
from .tools import turl
import re

homeurl = 'http://www.dybee.cn'

class logicDymf():

    # master调用
    def parseMas(self, redis, response):
        soup = BeautifulSoup(response.body.decode('utf-8', 'ignore'), 'lxml')

        pageInfo = soup.find('a', class_ = 'next page-numbers')
        if pageInfo is not None:
            redis.lpush('mysprider:urls_request', homeurl + pageInfo.get('href'))
            sleep(0.25)
            
        for urls in soup.find_all('a', target = '_blank', class_ = re.compile('user_list_(.*?)')):
            if urls is not None:
                strs = homeurl
                if urls.get('href').startswith(homeurl):
                    strs = urls.get('href')
                else:
                    strs += urls.get('href')
                redis.rpush('mysprider:urls_slaver', strs)

    # slaver调用
    def parseSla(self, redis, response):
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
                uonline = homeurl + uonline
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