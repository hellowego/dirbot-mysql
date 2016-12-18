#!/usr/bin/env python
#-*- coding: UTF-8 -*-
#
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

from dirbot.items import WebsiteLoader, Website

class Investor(BaseSpider):
    name = "investor"
    allowed_domains = ["zdb.pedaily.cn"]
    start_urls = [
        "http://zdb.pedaily.cn/company/all/"
        ]

    def parse(self, response):
        sites = response.css('#company-list')
        for site in sites:
