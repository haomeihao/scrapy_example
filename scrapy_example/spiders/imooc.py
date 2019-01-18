# -*- coding: utf-8 -*-

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_example.utils import *

class ImoocSpider(CrawlSpider):
    name = 'imooc'
    allowed_domains = ['www.imooc.com']
    start_urls = ['https://www.imooc.com/']

    custom_settings = {
        # request_depth_max 请求最大深度
        'DEPTH_LIMIT': 2,
        # verbose_stats 冗长统计
        'DEPTH_STATS_VERBOSE': True,
        # 深度优先策略 默认1
        'DEPTH_STATS': True,
        'DEPTH_PRIORITY ': 1,
        # 'SCHEDULER_DISK_QUEUE': 'scrapy.squeues.PickleFifoDiskQueue',
        'SCHEDULER_MEMORY_QUEUE': 'scrapy.squeues.FifoMemoryQueue',
    }

    rules = (
        Rule(LinkExtractor(allow=r'/course/list'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/course/list'), callback='sub_parse_item'),
    )

    def parse_item(self, response):
        i = {}
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        print(response.url, ', parse_item, ', response.meta['depth'])
        return i

    def sub_parse_item(self, response):
        i = {}
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        print(response.url, ', sub_parse_item, ', response.meta['depth'])
        return i


if __name__ == '__main__':
    pass