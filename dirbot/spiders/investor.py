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
        sites = response.css('#company-list > li > div.txt > h3')
        for site in sites:
            item = Investor()
            item['name'] = site.css(
                'a.f16::text').extract_first().strip()
            print item['name']