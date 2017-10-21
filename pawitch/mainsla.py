# -*- coding: utf-8 -*-
import os
import sys
from settings import MS_TYPE

def main():
    SlaverStart()


def SlaverStart():
    os.chdir('E:\\runtime\\Pywork\\myspider\\pawitch')
    os.system('scrapy crawl spridersla')
    print('------slaver started------')

if __name__=='__main__':
    main()