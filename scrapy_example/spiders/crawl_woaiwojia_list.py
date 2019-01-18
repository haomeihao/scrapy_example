# -*- coding: utf-8 -*-

# 修改默认编码规则 ascii -> utf-8
import sys

# reload(sys)
# sys.setdefaultencoding("utf-8")

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_example.utils import *


class WoaiwojiaSpider(CrawlSpider):
    name = 'crawl_woaiwojia_list'
    allowed_domains = ['bj.5i5j.com']
    start_urls = ['https://bj.5i5j.com/ershoufang/']
    custom_settings = {
        # cookie 自动传递 默认 False
        'COOKIES_ENABLED': False,
        # cookie debug日志打印 默认 False
        'COOKIES_DEBUG': True,

        # downloader 并发请求(concurrent requests)的最大值 默认32 会导致拉勾反爬虫 提示登录重定向
        'CONCURRENT_REQUESTS': 1,
        # downloader 在下载同一个网站下一个页面前需要等待的时间。该选项可以用来限制爬取速度， 减轻服务器压力
        'DOWNLOAD_DELAY': 3,

        # 用于检测过滤重复请求的类 默认 scrapy.dupefilter.RFPDupeFilter
        # 'DUPEFILTER_CLASS': 'scrapy.dupefilter.RFPDupeFilter',
        # 默认情况下， RFPDupeFilter 只记录第一次重复的请求。 设置 DUPEFILTER_DEBUG 为 True 将会使其记录所有重复的requests
        'DUPEFILTER_DEBUG': True,

        # 爬取网站最大允许的深度(depth)值。默认为0，没有限制
        'DEPTH_LIMIT': 3,
        # 整数值。用于根据深度调整 request 优先级。默认为0，不根据深度进行优先级调整 正值广度优先级别 负值深度优先级别
        # 默认 深度优先
        'DEPTH_PRIORITY': 1,
        'SCHEDULER_DISK_QUEUE': 'scrapy.squeues.PickleFifoDiskQueue',
        'SCHEDULER_MEMORY_QUEUE': 'scrapy.squeues.FifoMemoryQueue',
        # 是否收集最大深度数据 默认 True
        'DEPTH_STATS': True,
        # 是否收集详细的深度数据。如果启用，每个深度的请求数将会被收集在数据中 默认 False
        'DEPTH_STATS_VERBOSE': True,
    }

    rules = (
        Rule(LinkExtractor(allow=r'/ershoufang/n\w+/$'), callback='parse_list', follow=True),
        Rule(LinkExtractor(allow=r'/ershoufang/\d+.html$'), callback='parse_detail'),
    )

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.before_parse, dont_filter=True)

    def before_parse(self, response):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, dont_filter=True)

    def parse_start_url(self, response):
        return []

    def process_results(self, response, results):
        return results

    def parse_item(self, response):
        i = {}
        # i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        # i['name'] = response.xpath('//div[@id="name"]').extract()
        # i['description'] = response.xpath('//div[@id="description"]').extract()
        return i

    def parse_list(self, response):
        if not 200 <= response.status < 300:  # common case
            print("响应状态异常, parse_list, " + log_simple_response(response))
            return
        main_container = response.xpath('//div[@class="lfBox lf"]')
        if not main_container:
            print("响应页面有误, parse_list, " + log_simple_response(response))
            return
        print("爬取页面数据 parse_list, " + log_simple_response(response))

        house_total = main_container.xpath('//div[@class="total-box noBor"]/span/text()').extract_first()
        house_list_div = main_container.xpath('//div[@class="listCon"]')
        house_list = []
        for house_div in house_list_div:
            house_url = house_div.xpath('//h3/a/@href').extract_first()
            house_title = house_div.xpath('//h3/a/text()').extract_first()
            house_publish_date = house_div.xpath('//div[@class="listX"]/p/text()')[2].extract()
            house_info = {}
            house_info['house_url'] = house_url
            house_info['house_title'] = house_title
            house_info['house_publish_date'] = house_publish_date
            house_list.append(house_info)
        item = {}
        item['request_url'] = response.url
        item['house_total'] = int(house_total)
        # item['house_list'] = house_list
        yield item

    def parse_detail(self, response):
        if not 200 <= response.status < 300:  # common case
            print("响应状态异常, parse_detail, " + log_simple_response(response))
            return
        main_container = response.xpath('//div[@class="main container"]')
        if not main_container:
            print("响应页面有误, parse_detail, " + log_simple_response(response))
            return
        print("爬取页面数据 parse_detail, " + log_simple_response(response))

        house_title = main_container.xpath('//div[@class="rent-top fl"]/h1/text()').extract_first()
        house_desc = main_container.xpath('//div[@class="rent-top fl"]/p/text()').extract_first()
        house_id = house_desc.split('：')[-1]

        item = {}
        item['request_url'] = response.url
        item['house_id'] = house_id
        item['house_title'] = house_title
        item['house_desc'] = house_desc
        yield item

    def write_html_to_file(self, data, title):
        parent_dir = os.path.join(get_project_dir(), 'output/html/' + self.name + '/')
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir)
        time_str = str(get_second_timestamp())
        filename = parent_dir + time_str + '-' + title + '.html'
        with open(filename, 'w') as file:
            file.write(data)


if __name__ == '__main__':
    woaiwojia = WoaiwojiaSpider()
    woaiwojia.write_html_to_file(data='我学python', title='test')

    print(sys.getdefaultencoding())
