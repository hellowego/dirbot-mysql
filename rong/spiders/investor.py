#!/usr/bin/env python
#-*- coding: UTF-8 -*-
#
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from rong.items import WebsiteLoader, Website, InvestorItem
import time

class Investor(BaseSpider):
    name = "investor"
    allowed_domains = ["zdb.pedaily.cn"]
    start_urls = [
        "http://zdb.pedaily.cn/company/all/"
        ]

    def start_requests(self):
        # 1-10页没有公司头像的公司都没采集到
        # 101 - 201
        # 201 - 201     4019
        # 202 - 300     5995  有四条重复
        # 79197f1cfc1caebdbbbb453cb5a063ee, 95238540a5d97d7cc95e94b93be475dd, 7b37f246ebc639f9ea847622cd01a624, 1b8e761d617b32fb59d1d520b4d55812,
        # 301 - 301     6015  1865  4150
        # 302 - 302     6023  1868  4155   进来8个，12个重复
        # 303 - 400     7952  1947  6005    1980 相比301 进1937 tem 进1980， 1980-1937=43重复
        # 401 - 500     9951  2003  7948    3980  1个重复
        # 501 - 600     11935 2060 9875     5967
        page_num = 501
        while page_num < 601:
            print u'当前的页面编号: ', page_num
            str_page_name = str(page_num)+'/'
            if page_num == 1 :
                url = self.start_urls[0]
            else:
                url = self.start_urls[0] + str_page_name
            yield self.make_requests_from_url(url)
            page_num += 1
            time.sleep(3)



    # 解析投资机构城市、简介、公司名
    def parse(self, response):
        # sites = response.css('#company-list > li > div.txt')
        sites = response.css('#company-list > li')
        for site in sites:
            item = InvestorItem()
            try:
                item['source_url'] = response.url
                item['name'] = site.css(
                    'a.f16::text').extract_first().strip()
                try:
                    item['name_abbr'] = site.xpath(
                        './/span/a/text()').extract_first().strip()
                except:
                    item['name_abbr'] = ''

                try:
                    item['company_desc'] = site.css(
                        'div.desc::text').extract_first().strip()
                except:
                    item['company_desc'] = ''

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