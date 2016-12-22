#!/usr/bin/env python
#-*- coding: UTF-8 -*-
#
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from dirbot.items import WebsiteLoader, Website, InvestorItem
import time

class Investor(BaseSpider):
    name = "investor"
    allowed_domains = ["zdb.pedaily.cn"]
    start_urls = [
        "http://zdb.pedaily.cn/company/all/"
        ]

    def start_requests(self):
        # 1-10页没有公司头像的公司都没采集到
        page_num = 11
        while page_num < 100:
            print u'当前的页面编号: ', page_num
            str_page_name = str(page_num)+'/'
            url = self.start_urls[0] + str_page_name
            yield self.make_requests_from_url(url)
            page_num += 1
            time.sleep(5)



    # 解析投资机构城市、简介、公司名
    def parse(self, response):
        # sites = response.css('#company-list > li > div.txt')
        sites = response.css('#company-list > li')
        for site in sites:
            item = InvestorItem()
            try:
                item['name'] = site.css(
                    'a.f16::text').extract_first().strip()
                item['name_abbr'] = site.xpath(
                    './/span/a/text()').extract_first().strip()
                item['company_desc'] = site.css(
                    'div.desc::text').extract_first().strip()
                str = site.css(
                    'a::attr(href)').extract_first().strip()
                item['detail_url'] = str
                str1 = site.css(
                    'img::attr(src)').extract_first().strip()
                item['img_url'] = str1
                # 有的会没city，会报错
                try:
                    item['city'] = site.xpath(
                        './/span/text()').extract_first().strip()
                except:
                    item['city'] = ''
            except (TypeError, IndexError):
                continue
            yield item