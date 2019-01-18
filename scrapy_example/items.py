# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyExampleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class WoaiwojiaHouseItem(scrapy.Item):
    request_url = scrapy.Field()
    house_id = scrapy.Field()
    house_title = scrapy.Field()
    house_publish_date = scrapy.Field()
    plate_name = scrapy.Field()
    house_city = scrapy.Field()
    house_region = scrapy.Field()
    house_address = scrapy.Field()
    house_village = scrapy.Field()
    sell_price = scrapy.Field()
    sell_price_unit = scrapy.Field()
    unit_price = scrapy.Field()
    unit_price_unit = scrapy.Field()
    crawl_time = scrapy.Field()

