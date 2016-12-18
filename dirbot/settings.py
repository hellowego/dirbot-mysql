# Scrapy settings for dirbot project

SPIDER_MODULES = ['dirbot.spiders']
NEWSPIDER_MODULE = 'dirbot.spiders'
DEFAULT_ITEM_CLASS = 'dirbot.items.Website'

ITEM_PIPELINES = {
    'dirbot.pipelines.RequiredFieldsPipeline': 1,
    'dirbot.pipelines.FilterWordsPipeline' :2,
    'dirbot.pipelines.MySQLStorePipeline':3,
}

MYSQL_HOST = 'localhost'
MYSQL_DBNAME = 'rong'
MYSQL_USER = 'root'
MYSQL_PASSWD = 'root'
