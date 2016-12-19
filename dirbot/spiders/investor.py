#!/usr/bin/env python
#-*- coding: UTF-8 -*-
#
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

from dirbot.items import WebsiteLoader, Website, InvestorItem

class Investor(BaseSpider):
    name = "investor"
    allowed_domains = ["zdb.pedaily.cn"]
    start_urls = [
        "http://zdb.pedaily.cn/company/all/"
        ]

    # 解析投资机构城市、简介、公司名
    def parse(self, response):
        sites = response.css('#company-list > li > div.txt')
        for site in sites:
            item = InvestorItem()
            item['city'] = site.xpath(
                './/span[1]/text()').extract_first().strip()
            item['company_name'] = site.css(
                'a.f16::text').extract_first().strip()
            item['company_desc'] = site.css(
                'div.desc::text').extract_first().strip()
            yield item