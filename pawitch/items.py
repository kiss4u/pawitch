# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PawitchItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class NextUrlsItem(scrapy.Item):
    seq = scrapy.Field() 
    title = scrapy.Field()
    url = scrapy.Field()
    pass

class MovieItem(scrapy.Item):
    title = scrapy.Field()
    pic = scrapy.Field()
    download = scrapy.Field()
    introduce = scrapy.Field()
    pass