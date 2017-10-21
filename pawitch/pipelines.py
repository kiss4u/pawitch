# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pawitch import settings

class PawitchPipelineMaster(object):

    # 取待爬URL存到redis-request中待爬取
    # 已完成的存到redis-filter中过滤
    def process_item(self, item, spider):
        if settings.MS_TYPE == 'type_master':
            print('pip--------m')
        return item



class PawitchPipelineSlaver(object):
    def process_item(self, item, spider):
        if settings.MS_TYPE == 'type_slaver':
            print('pip--------s')
        return item
