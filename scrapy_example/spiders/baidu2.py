# -*- coding: utf-8 -*-

import scrapy
from scrapy.http.request import Request
from scrapy_example.utils import *


class Baidu2Spider(scrapy.Spider):
    name = 'baidu2'
    allowed_domains = ['www.baidu.com']
    start_urls = ['https://www.baidu.com']
    custom_settings = {
        'COOKIES_ENABLED': True,
        'DUPEFILTER_DEBUG': True,
        'DEPTH_LIMIT': 3,
        'CONCURRENT_REQUESTS': 1,
        'DOWNLOAD_DELAY': 1,
    }

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, cookies={'xxx.com': 'true'}, callback=self.parse, dont_filter=True)

    def parse(self, response):
        # console(response.request.headers, 'parse.response.request.headers')
        # write_html_to_file(response.text, 'parse.response.text', self.name)

        for url in self.start_urls:
            yield Request(url, cookies={'yyy.com': 'true'},
                          callback=self.sub_parse)

    def sub_parse(self, response):
        # console(response.request.headers, 'sub_parse.response.request.headers')
        # write_html_to_file(response.text, 'sub_parse.response.text', self.name)

        response_request_headers = response.request.headers
        for url in self.start_urls:
            yield Request(url, headers=response_request_headers, cookies={'zzz.com': 'true'},
                          callback=self.sub_sub_parse)

    def sub_sub_parse(self, response):
        # console(response.request.headers, 'sub_sub_parse.response.request.headers')
        # write_html_to_file(response.text, 'sub_sub_parse.response.text', self.name)

        self.log('一切都结束了...')


if __name__ == '__main__':
    pass
