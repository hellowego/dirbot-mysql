# Scrapy settings for rong project

SPIDER_MODULES = ['rong.spiders']
NEWSPIDER_MODULE = 'rong.spiders'
DEFAULT_ITEM_CLASS = 'rong.items.Website'

ITEM_PIPELINES = {
    'rong.pipelines.RequiredFieldsPipeline': 1,
    'rong.pipelines.DownloadImgPipeline':3,
    'rong.pipelines.MySQLStoreInvestorPipeline':4,
}

MYSQL_HOST = 'localhost'
MYSQL_DBNAME = 'rong'
MYSQL_USER = 'root'
MYSQL_PASSWD = 'root'
