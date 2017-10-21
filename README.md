## pawitch
#分布式爬虫系统


1、需要安装'Redis'和'MySQL'
2、配置settings.py中'MS_TYPE'区分主从
3、执行main.py启动
4、Redis需插入lpush mysprider:urls_request 地址，可放入启动脚本做定时
