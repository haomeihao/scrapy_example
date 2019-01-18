# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from scrapy_example.utils import *


class Woaiwojia3Spider(CrawlSpider):
    name = 'woaiwojia3'
    allowed_domains = ['bj.5i5j.com']
    start_urls = ['https://bj.5i5j.com/ershoufang/']
    custom_settings = {
        # 不要默认，设置1 默认是0.5-1.5
        # 'AUTOTHROTTLE_ENABLED': True,
        'DOWNLOAD_DELAY': 1,
        # 不要默认，设置小点 默认是32
        'CONCURRENT_REQUESTS': 1,
        # 深度级别设置
        # 'DEPTH_LIMIT': 3,
        # 'DEPTH_PRIORITY ': 1,
        # 'SCHEDULER_DISK_QUEUE': 'scrapy.squeues.PickleFifoDiskQueue',
        # 'SCHEDULER_MEMORY_QUEUE': 'scrapy.squeues.FifoMemoryQueue',
        # url 去重 开启 debug 模式
        # 'DUPEFILTER_CLASS': 'scrapy.dupefilters.RFPDupeFilte',
        'DUPEFILTER_DEBUG': True
    }

    # 好像 和 CONCURRENT_REQUESTS 效果一样
    every_request_delay = 0
    total_page_no = 5
    every_sub_page_no = 10
    plate_name = '二手房'
    response_request_headers = {}

    Rule = (
        Rule(LinkExtractor(allow=("ershoufang/n\d",)), follow=True),
        Rule(LinkExtractor(allow=r'ershoufang/\d+.html'), callback='parse_house', follow=True),
    )

    def parse_house(self, response):
        code = response.status
        if not code == 200:
            print(log_now_time() + "请求失败 parse_house response.status: " + code)
            return None
        print(log_now_time() + "请求成功 parse_house response.url: " + response.url)


if __name__ == '__main__':
    pass
