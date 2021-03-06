from scrapy.item import Item, Field
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import TakeFirst


class Website(Item):
    name = Field()
    description = Field()
    url = Field()


class WebsiteLoader(XPathItemLoader):
    default_item_class = Website
    default_output_processor = TakeFirst()


class InvestorItem(Item):
    city = Field()
    name = Field()
    name_abbr = Field()
    company_desc = Field()
    detail_url = Field()
    img_url = Field()
    img_name = Field()
    img_location = Field()
    introduce = Field()
    guid = Field()
    source_url = Field()