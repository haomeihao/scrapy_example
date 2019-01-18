# -*- coding: utf-8 -*-

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_example.utils import parse_to_dict


class ImoocSpider(CrawlSpider):
    name = 'crawl_imooc'
    allowed_domains = ['coding.imooc.com']
    start_urls = ['https://coding.imooc.com/']
    custom_settings = {
        # cookie 自动传递 默认 False
        'COOKIES_ENABLED': False,
        # cookie debug日志打印 默认 False
        'COOKIES_DEBUG': True,

        # downloader 并发请求(concurrent requests)的最大值 默认32 会导致拉勾反爬虫 提示登录重定向
        'CONCURRENT_REQUESTS': 1,
        # downloader 在下载同一个网站下一个页面前需要等待的时间。该选项可以用来限制爬取速度， 减轻服务器压力
        'DOWNLOAD_DELAY': 5,

        # 用于检测过滤重复请求的类 默认 scrapy.dupefilter.RFPDupeFilter
        # 'DUPEFILTER_CLASS': 'scrapy.dupefilter.RFPDupeFilter',
        # 默认情况下， RFPDupeFilter 只记录第一次重复的请求。 设置 DUPEFILTER_DEBUG 为 True 将会使其记录所有重复的requests
        'DUPEFILTER_DEBUG': True,

        # 爬取网站最大允许的深度(depth)值。默认为0，没有限制
        'DEPTH_LIMIT': 2,
        # 整数值。用于根据深度调整 request 优先级。默认为0，不根据深度进行优先级调整 正值广度优先级别 负值深度优先级别
        # 默认 深度优先
        'DEPTH_PRIORITY': 0,
        'SCHEDULER_DISK_QUEUE': 'scrapy.squeues.PickleFifoDiskQueue',
        'SCHEDULER_MEMORY_QUEUE': 'scrapy.squeues.FifoMemoryQueue',
        # 是否收集最大深度数据 默认 True
        'DEPTH_STATS': True,
        # 是否收集详细的深度数据。如果启用，每个深度的请求数将会被收集在数据中 默认 False
        'DEPTH_STATS_VERBOSE': True,
    }

    rules = (
        Rule(LinkExtractor(allow=r'/?sort=1&unlearn=0&page=\d+'), callback='parse_page', follow=True),
        Rule(LinkExtractor(allow=r'/class/\d+.html$'), callback='parse_class'),
        Rule(LinkExtractor(allow=r'/learn/list/\d+.html$'), callback='parse_learn_list'),
    )

    def parse_item(self, response):
        i = {}
        # i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        # i['name'] = response.xpath('//div[@id="name"]').extract()
        # i['description'] = response.xpath('//div[@id="description"]').extract()
        return i

    def parse_page(self, response):
        i = {}
        self.print_info(response, 'page')
        return i

    def parse_class(self, response):
        i = {}
        self.print_info(response, 'class')
        return i

    def parse_learn_list(self, response):
        i = {}
        self.print_info(response, 'learn-list')
        return i

    def print_info(self, response, title):
        res_req_headers = parse_to_dict(response.request.headers)
        print(title + ' response successfully, ' + response.url + ', depth: ' + str(
            response.meta.get('depth')) + ', referer: ' + res_req_headers.get('Referer'))
