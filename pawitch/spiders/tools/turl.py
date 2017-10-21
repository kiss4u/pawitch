# -*- coding: utf-8 -*-    
import urllib.request
import json

def urlToShort(url_long):
    try:
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'} 
        appKey = 3271760578 #
        #http://api.t.sina.com.cn/short_url/shorten.json?source=3271760578&url_long=http://www.dybee.cn/17930.html
        sapi = 'http://api.t.sina.com.cn/short_url/shorten.json?source=%s&url_long=%s' % (appKey, url_long)

        req = urllib.request.Request(url=sapi, headers=headers)
        content = urllib.request.urlopen(req).read().decode('utf-8')
        result = json.loads(content)
        url_short = result[0].get('url_short')
        #print(url_short)
        return url_short
    except:
        return ''
    

if __name__ == '__main__':  

    urlToShort('http://www.dybee.cn/playm3u8/?url=http://fuli.zuida-youku-le.com/20170828/NRROcxOP/index.m3u8')