# -*- coding: utf-8 -*-
from urllib import parse

import scrapy
from scrapy.http.request import Request
from scrapy_example.utils import *


class WoaiwojiaSpider(scrapy.Spider):
    name = 'woaiwojia'
    allowed_domains = ['bj.5i5j.com']
    start_urls = ['https://bj.5i5j.com/ershoufang/']
    custom_settings = {
        # 不要默认，设置1 默认是0.5-1.5
        'AUTOTHROTTLE_ENABLED': True,
        # 'DOWNLOAD_DELAY': 1,
        # 不要默认，设置小点 默认是32
        'CONCURRENT_REQUESTS': 1,

        # 请求最大深度 默认0 不限制
        # class scrapy.spidermiddlewares.depth.DepthMiddleware
        'DEPTH_LIMIT': 3,
        # verbose_stats 冗长统计
        'DEPTH_STATS': True,
        'DEPTH_STATS_VERBOSE': True,
        # 深度优先策略 默认0不处理 正值先进行广度爬行 负值先进行深度爬行
        'DEPTH_PRIORITY ': -1,
        # 'SCHEDULER_DISK_QUEUE': 'scrapy.squeues.PickleFifoDiskQueue',
        'SCHEDULER_MEMORY_QUEUE': 'scrapy.squeues.FifoMemoryQueue',

        # url 去重 开启 debug 模式
        'DUPEFILTER_CLASS': 'scrapy.dupefilters.RFPDupeFilter',
        'DUPEFILTER_DEBUG': True
    }

    # 好像 和 CONCURRENT_REQUESTS 效果一样
    every_request_delay = 2
    total_page_no = 5
    every_sub_page_no = 5
    plate_name = '二手房'
    response_request_headers = {}

    def get_depth(self):
        return self.settings.get('DEPTH_LIMIT', 0)

    def start_requests(self):
        print(log_now_time() + self.name + " spider depth: " + str(self.get_depth()))
        self.log(log_now_time() + self.name + " spider depth: " + str(self.get_depth()))

        for url in self.start_urls:
            yield Request(url, cookies={'xxx.com': 'true'}, callback=self.parse)

    def parse(self, response):
        # console(response.request.headers, 'parse.response.request.headers', self.name)
        # write_html_to_file(response.text, 'parse.response.text', self.name)
        # response_request_headers = response.request.headers

        for url in self.start_urls:
            yield Request(url, cookies={'yyy.com': 'true'},
                          callback=self.sub_parse, dont_filter=True)

    def sub_parse(self, response):
        code = response.status
        if not 200 <= code < 300:
            print(log_now_time() + "响应失败 sub_parse response.status: " + code)
            self.log("响应失败 sub_parse response.status: " + code)
            response.meta['depth'] = 1
            # return Request(url=response.url, callback=self.sub_parse, cookies={'retry.com': 'true'})
            return None
        print(log_now_time() + "响应成功 sub_parse response.url: " + response.url)

        # console(response.request.headers, 'sub_parse.response.request.headers', self.name)
        # write_html_to_file(response.text, 'sub_parse.response.text', self.name)
        self.response_request_headers = response.request.headers

        # 当前页 重要数据
        total_house_div = response.css("div.total-box")
        if not total_house_div:
            print("sub_parse() 失败...")
            self.log("sub_parse() 失败...")
            return None
        total_house_number = total_house_div.css("span::text").extract_first()
        # print(log_now_time() + "共找到 " + total_house_number + " 套房源")
        # 当前页 分页条
        page_div = response.css("div.pageSty")[0]
        current_page_no = page_div.css("a.cur::text").extract_first()

        # 房源详情页访问
        list_house_div = response.css("div.listCon")
        sub_page_no = 1
        meta = {}
        for house_div in list_house_div:
            list_title_div = house_div.css("h3.listTit")[0]
            list_desc_div = house_div.css("div.listX")[0]
            house_href = list_title_div.css("a::attr(href)").extract_first()
            house_title = list_title_div.css("a::text").extract_first()
            house_publish_date_str = list_desc_div.css("p")[2].css("::text").extract_first()
            house_publish_date = house_publish_date_str.split('·')[-1].strip()[0:-2]
            if house_href is not None:
                if sub_page_no > self.every_sub_page_no:
                    # print(log_now_time() + "第 " + current_page_no + " 页只处理 " + str(self.every_sub_page_no) + "条数据")
                    break
                meta['house_publish_date'] = house_publish_date

                time.sleep(self.every_request_delay)
                print(log_now_time() + "开始请求详情页: " + house_href)
                # 重要自己控制深度
                response.meta['depth'] = 2
                yield Request(url=parse.urljoin(response.url, house_href), callback=self.sub_sub_parse,
                              headers=self.response_request_headers,
                              cookies={'zzz.com': 'true'}, meta=meta)
            sub_page_no += 1

            if int(self.get_depth()) <= 2:
                yield {
                    'depth': 2,
                    'request_url': response.url,
                    'house_title': house_title,
                    'house_publish_date': house_publish_date,
                    'plate_name': self.plate_name,
                    'crawl_time': format_now_time()
                }

        # 下一页访问
        next_page_href = page_div.css("a.cPage::attr(href)").extract_first()
        if next_page_href is not None:
            # print(log_now_time() + "当前页数:" + current_page_no + ", 下一页: " + next_page_href)
            self.log("当前页数:" + current_page_no + ", 下一页: " + next_page_href)
            if int(current_page_no) >= self.total_page_no:
                # print(log_now_time() + "一切都提前结束了...")
                self.log("一切都提前结束了...")
                return None

            time.sleep(self.every_request_delay)
            print(log_now_time() + "开始请求下一页: " + next_page_href)
            # 重要自己控制深度
            response.meta['depth'] = 1
            yield Request(url=parse.urljoin(response.url, next_page_href), callback=self.sub_parse,
                          headers=self.response_request_headers,
                          cookies={'zzz.com': 'true'})

    def sub_sub_parse(self, response):
        code = response.status
        if not 200 <= code < 300:
            print(log_now_time() + "响应失败 sub_sub_parse response.status: " + code)
            self.log("响应失败 sub_sub_parse response.status: " + code)
            response.meta['depth'] = 2
            # return Request(url=response.url, callback=self.sub_sub_parse, cookies={'retry.com': 'true'})
            return None
        print(log_now_time() + "响应成功 sub_sub_parse response.url: " + response.url)

        # console(response.request.headers, 'sub_sub_parse.response.request.headers', self.name)
        # write_html_to_file(response.text, 'sub_sub_parse.response.text', self.name)
        self.response_request_headers = response.request.headers

        house_publish_date = response.meta.get('house_publish_date', '')
        house_title_div = response.css("div.rent-top")[0]
        house_title = house_title_div.css("h1.house-tit::text").extract_first().strip()
        house_desc = house_title_div.css("p::text").extract_first()
        house_id = house_desc.split('|')[-1].split('：')[-1].strip()

        house_city_div = response.css("div.top-city")[0]
        house_city = house_city_div.css("::text").extract_first().strip()
        list_house_path = response.css("div.cur-path")
        plate_length = len(self.plate_name)
        house_region_str = list_house_path.css("a")[2].css("::text").extract_first()
        house_region = house_region_str.strip()[0:-plate_length]
        house_address_str = list_house_path.css("a")[3].css("::text").extract_first()
        house_address = house_address_str.strip()[0:-plate_length]
        house_village_str = list_house_path.css("a")[4].css("::text").extract_first()
        house_village = house_village_str.strip()[0:-plate_length]

        house_sell_info = response.css("div.housesty")[0]
        sell_price = house_sell_info.css("p.jlinfo")[0].css("::text").extract_first().strip()
        unit_price = house_sell_info.css("p.jlinfo")[1].css("::text").extract_first().strip()

        print(log_now_time() + "Crawled Scraped success from url: " + response.url)

        if int(self.get_depth()) <= 3:
            yield {
                'depth': 3,
                'request_url': response.url,
                'house_id': house_id,
                'house_title': house_title,
                'house_publish_date': house_publish_date,
                'plate_name': self.plate_name,
                'house_city': house_city,
                'house_region': house_region,
                'house_address': house_address,
                'house_village': house_village,
                'sell_price': float(sell_price),
                'sell_price_unit': '(万)',
                'unit_price': float(unit_price),
                'unit_price_unit': '(万/m²)',
                'crawl_time': format_now_time()
            }


if __name__ == '__main__':
    pass
