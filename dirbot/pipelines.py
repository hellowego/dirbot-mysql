#!/usr/bin/env python
#-*- coding: UTF-8 -*-
from datetime import datetime
from hashlib import md5
from scrapy import log
from scrapy.exceptions import DropItem
from twisted.enterprise import adbapi
from dbSession import DBSession
from dbModel import InvestorModel, InvestorTemModelTem
import os
import urllib
import urlparse
import time


class RequiredFieldsPipeline(object):
    """A pipeline to ensure the item have the required fields."""

    required_fields = ('name', 'detail_url', 'img_url')

    def process_item(self, item, spider):
        # 检查必须的字段
        for field in self.required_fields:
            if not item.get(field):
                raise DropItem("Field '%s' missing: %r" % (field, item))

        # 取公司名的md5作为guid和公司图标的名字
        item['guid'] =self._get_guid(item)
        return item

    def _get_guid(self, item):
        """Generates an unique identifier for a given item."""
        # hash based solely in the url field
        str = item['name']
        return md5(str.encode("utf8")).hexdigest()

class DownloadImgPipeline(object):
    '''
    下载投资公司头像图片
    '''
    def process_item(self, item, spider):
        # 如果没有企业头像，则不需要下载，采用默认头像
        img_url = item.get('img_url')
        item['img_location'] = u'company-icon'
        web_img_name = self.get_imgName(img_url)
        if web_img_name == 'noimage.png' :
            item['img_name'] = 'noimage.png'
            return item
        img_suffix = os.path.splitext(web_img_name)[1]
        item['img_name'] = item['guid'] + img_suffix
        path = os.path.join(os.getcwd(), item['img_location'])
        self.download(item['img_name'], img_url, path)
        return item

    def get_imgName(self, url):
        img_parse = urlparse.urlparse(url)
        return os.path.basename(img_parse.path)


    def download(self, img_name, img_url, path):
        if not os.path.exists(path):
            os.mkdir(path)
        homedir = os.path.join(path, img_name)
        if not os.path.exists(homedir):
            with open(homedir, 'wb') as img_writer:
                conn = urllib.urlopen(img_url) #下载图片
                img_writer.write(conn.read())
                img_writer.close()


    def img_exist(self):
        session = DBSession()
        # count = session.execute('select * from investor where guid = :guid', {'guid' : 1})
        count = session.query(InvestorModel).filter(InvestorModel.guid == '1').count()
        session.close()
        print count

class MySQLStoreInvestorPipeline(object):
    def process_item(self, item, spider):
        investor = InvestorModel(guid =item['guid']
                                 , city = item['city']
                                 , company_desc = item['company_desc']
                                 , detail_url = item['detail_url']
                                 , img_name = item['img_name']
                                 , img_url = item['img_url']
                                 , img_location = item['img_location']
                                 , name = item['name']
                                 , name_abbr = item['name_abbr']
                                 )
        investorTemModelTem = InvestorTemModelTem(guid =item['guid']
                                 , city = item['city']
                                 , company_desc = item['company_desc']
                                 , detail_url = item['detail_url']
                                 , img_name = item['img_name']
                                 , img_url = item['img_url']
                                 , img_location = item['img_location']
                                 , name = item['name']
                                 , name_abbr = item['name_abbr']
                                 )
        session = DBSession()
        session.merge(investor)
        session.add(investorTemModelTem)
        session.commit()
        session.close()

class InvestorRecord(object):
    def process_item(self, item, spider):
        # 获取图片url
        img_url = item.get('img_url')
        if img_url is not None :
            pass

        return item

class FilterWordsPipeline(object):
    """A pipeline for filtering out items which contain certain words in their
    description"""

    # put all words in lowercase
    words_to_filter = ['politics', 'religion']

    def process_item(self, item, spider):
        for word in self.words_to_filter:
            desc = item.get('description') or ''
            if word in desc.lower():
                raise DropItem("Contains forbidden word: %s" % word)
        else:
            return item







class MySQLStorePipeline(object):
    """A pipeline to store the item in a MySQL database.

    This implementation uses Twisted's asynchronous database API.
    """

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)

    def process_item(self, item, spider):
        # run db query in the thread pool
        d = self.dbpool.runInteraction(self._do_upsert, item, spider)
        d.addErrback(self._handle_error, item, spider)
        # at the end return the item in case of success or failure
        d.addBoth(lambda _: item)
        # return the deferred instead the item. This makes the engine to
        # process next item (according to CONCURRENT_ITEMS setting) after this
        # operation (deferred) has finished.
        return d

    def _do_upsert(self, conn, item, spider):
        """Perform an insert or update."""
        guid = self._get_guid(item)
        now = datetime.utcnow().replace(microsecond=0).isoformat(' ')

        conn.execute("""SELECT EXISTS(
            SELECT 1 FROM website WHERE guid = %s
        )""", (guid, ))
        ret = conn.fetchone()[0]

        if ret:
            conn.execute("""
                UPDATE website
                SET name=%s, description=%s, url=%s, updated=%s
                WHERE guid=%s
            """, (item['name'], item['description'], item['url'], now, guid))
            spider.log("Item updated in db: %s %r" % (guid, item))
        else:
            conn.execute("""
                INSERT INTO website (guid, name, description, url, updated)
                VALUES (%s, %s, %s, %s, %s)
            """, (guid, item['name'], item['description'], item['url'], now))
            spider.log("Item stored in db: %s %r" % (guid, item))

    def _handle_error(self, failure, item, spider):
        """Handle occurred on db interaction."""
        # do nothing, just log
        log.err(failure)

    def _get_guid(self, item):
        """Generates an unique identifier for a given item."""
        # hash based solely in the url field
        return md5(item['url']).hexdigest()

if __name__ == "__main__":
    dl = DownloadImgPipeline()

    img_url = u'http://pic.pedata.cn/Logo/Logo/ab55f75f-7d36-4939-aade-83691372b86d.gif'

    s1 = urlparse.urlparse(img_url)
    s2 = s1.path
    print s1
    print s2
    s3 = os.path.basename(s2)
    print s3
    # 分离扩展名
    s4 = os.path.splitext(s2)
    print s4[0], s4[1]
    s5 = u'hello您好'
    s6 = md5(s5.encode('utf8')).hexdigest()
    print s5, s6
    print s6 + '.png'
    img_name = s6 + s4[1]
    path = os.getcwd()
    img_location = u'company-icon'
    path = os.path.join(os.getcwd(), img_location)
    print img_name
    print path
    dl.download(img_name, img_url, path)

    # dl.img_exist()