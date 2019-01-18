# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class Bj5i5jSpider(CrawlSpider):
    name = 'bj5i5j'
    allowed_domains = ['bj.5i5j.com']
    start_urls = ['https://bj.5i5j.com/']

    custom_settings = {
        'DEPTH_LIMIT': 2,
    }

    rules = (
        Rule(LinkExtractor(allow=r'/ershoufang/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        i = {}
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        print(response.url)
        return i
