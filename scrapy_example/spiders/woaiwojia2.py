# -*- coding: utf-8 -*-

import scrapy
from scrapy.http.request import Request
from scrapy.loader import ItemLoader

from scrapy_example.utils import *
from scrapy_example.items import WoaiwojiaHouseItem

class Woaiwojia2Spider(scrapy.Spider):
    name = 'woaiwojia2'
    allowed_domains = ['bj.5i5j.com']
    start_urls = ['https://bj.5i5j.com/ershoufang/']
    custom_settings = {
        # 不要默认，设置1 默认是0.5-1.5
        # 'AUTOTHROTTLE_ENABLED': True,
        'DOWNLOAD_DELAY': 0.5,
        # 不要默认，设置小点 默认是32
        'CONCURRENT_REQUESTS': 8,
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

    def start_requests(self):
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
        if not code == 200:
            print(log_now_time() + "请求失败 sub_parse response.status: " + code)
            self.log("请求失败 sub_parse response.status: " + code)
            return None
        print(log_now_time() + "请求成功 sub_parse response.url: " + response.url)

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
        print(log_now_time() + "共找到 " + total_house_number + " 套房源")
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
                    print(log_now_time() + "第 " + current_page_no + " 页只处理 " + str(self.every_sub_page_no) + "条数据")
                    break
                # print(log_now_time() + house_title + ", " + house_href + ", " + house_publish_date)
                meta['house_publish_date'] = house_publish_date
                time.sleep(self.every_request_delay)
                print(log_now_time() + "开始请求详情页: " + house_href)
                yield response.follow(url=house_href, callback=self.sub_sub_parse,
                                      headers=self.response_request_headers,
                                      cookies={'zzz.com': 'true'}, meta=meta)
            sub_page_no += 1

        # 下一页访问
        next_page_href = page_div.css("a.cPage::attr(href)").extract_first()
        if next_page_href is not None:
            print(log_now_time() + "当前页数:" + current_page_no + ", 下一页: " + next_page_href)
            self.log("当前页数:" + current_page_no + ", 下一页: " + next_page_href)
            if int(current_page_no) >= self.total_page_no:
                print(log_now_time() + "一切都提前结束了...")
                self.log("一切都提前结束了...")
                return None
            time.sleep(self.every_request_delay)
            print(log_now_time() + "开始请求下一页: " + next_page_href)
            yield response.follow(url=next_page_href, callback=self.sub_parse,
                                  headers=self.response_request_headers,
                                  cookies={'zzz.com': 'true'})

    def sub_sub_parse(self, response):
        code = response.status
        if not code == 200:
            print(log_now_time() + "请求失败 sub_sub_parse response.status: " + code)
            self.log("请求失败 sub_sub_parse response.status: " + code)
            return None
        print(log_now_time() + "请求成功 sub_sub_parse response.url: " + response.url)

        # console(response.request.headers, 'sub_sub_parse.response.request.headers', self.name)
        # write_html_to_file(response.text, 'sub_sub_parse.response.text', self.name)
        self.response_request_headers = response.request.headers

        item_loader = ItemLoader(item=WoaiwojiaHouseItem(), response=response)
        house_publish_date = response.meta['house_publish_date']

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

        print(log_now_time() + "Crawled Scraped success from: " + response.url)

        item_loader.add_value('request_url', response.url)
        item_loader.add_value('house_id', house_id)
        item_loader.add_value('house_title', house_title)
        item_loader.add_value('house_publish_date', house_publish_date)
        item_loader.add_value('plate_name', self.plate_name)
        item_loader.add_value('house_city', house_city)
        item_loader.add_value('house_region', house_region)
        item_loader.add_value('house_address', house_address)
        item_loader.add_value('house_village', house_village)
        item_loader.add_value('sell_price', float(sell_price))
        item_loader.add_value('sell_price_unit', "(万)")
        item_loader.add_value('unit_price', float(unit_price))
        item_loader.add_value('unit_price_unit', "(万/m²)")
        item_loader.add_value('crawl_time', datetime.datetime.now())

        yield item_loader.load_item()


if __name__ == '__main__':
    pass