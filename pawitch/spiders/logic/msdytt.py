# -*- coding: utf-8 -*-
import re
from time import sleep
from bs4 import BeautifulSoup
from ..tools import *

homeurl = 'http://www.dytt8.net/'

class logicDytt():

    def replace_chara(markup):
        return markup.replace(u'\xa0' , u' ')

    def parseMas(self, redis, response):
        # 页面跳转信息
        soup = BeautifulSoup(response.body.decode('gb2312', 'ignore'), 'lxml')
        for pageInfo in soup.find_all('div', class_='x'):
            pageUrl = re.findall(r'<a href="(.*?)">.*</a>', repr(pageInfo))
            if pageUrl != []:
                redis.lpush('mysprider:urls_request', homeurl + 'html/gndy/dyzz/' + pageUrl[-2])

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
                redis.rpush('mysprider:urls_slaver', homeurl + slaverurl[0])


    def parseSla(self, redis, response):
        soup = BeautifulSoup(response.body.decode('gb2312', 'ignore'), 'lxml')
    
        #saveToFile(soup)

        #取迅雷地址
        url = soup.find('td', style="WORD-WRAP: break-word").get_text()
        name = soup.find('title').get_text()
        # print(soup.find('td', style="WORD-WRAP: break-word"))
        # print(soup.find('title'))

        db = tmysql.Mysql()
        #sql = 'insert into filminfo(fid, name, download, introduce) values (1,"22222","")'
        attrs = ['name', 'udownload', 'introduce']
        value = [str(name), str(url), '']
        db._insert('filminfo', attrs, value)
        
        #re.compile('thunder:.*=')
        #爬取成功存到已爬取
        redis.sadd('mysprider:urls_filter', response.url)

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
