# -*- coding: utf-8 -*-
import os
import sys
sys.path.append("..")
from settings import MS_TYPE

def main():
    if MS_TYPE == 'type_master':
        MasterStart()
    elif MS_TYPE == 'type_slaver':
        SlaverStart()
    else:
        print('------start failed, setting error------')


def MasterStart():
    os.chdir('E:\\runtime\\Pywork\\myspider\\pawitch')
    os.system('scrapy crawl spridermas')
    print('------master started------')

def SlaverStart():
    os.chdir('E:\\runtime\\Pywork\\myspider\\pawitch')
    os.system('scrapy crawl spridersla')
    print('------slaver started------')

if __name__=='__main__':
    main()