# -*- coding: utf-8 -*-

from urllib import parse
from scrapy.http.request import Request
from scrapy_redis.spiders import RedisSpider

from scrapy_example.utils import *
from scrapy_example.redis_spiders import CustomRedisSpider


class WoaiwojiaListSpider(CustomRedisSpider):
    name = 'woaiwojia_list'
    # 注意一定要写
    parent_name = ''
    sub_name = 'woaiwojia_detail'

    allowed_domains = ['bj.5i5j.com']
    # start_urls = ['https://bj.5i5j.com/ershoufang/']
    redis_key = name + ':start_urls'
    # RPUSH woaiwojia_list:start_urls https://bj.5i5j.com/ershoufang/

    custom_settings = {
        'DOWNLOAD_DELAY': 3
    }
    meta = {'dont_merge_cookies': True}
    # 好像 和 CONCURRENT_REQUESTS 效果一样
    every_request_delay = 0
    total_page_no = 5
    every_sub_page_no = 5
    plate_name = '二手房'

    def parse(self, response):
        # if not 200 <= response.status < 300:
        #     print_log_error(title='Response Status is Exception, ', content=log_simple_response(response))
        #     yield Request(url=response.url, callback=self.parse, meta=self.meta)
        #     return

        # write_html_to_file(response.text, str(get_time_stamp()), self.name)

        total_house_div = response.css("div.total-box")
        if not total_house_div:
            print_log_error(title='Response Html is Wrong, ', content=log_simple_response(response))
            # push retry url
            self.sadd_fail_url(response.url)
            # yield Request(url=response.url, callback=self.parse)
            return

        print_log_info(title='Response Successfully, ', content=log_simple_response(response))

        # 房源详情页访问
        house_list_div = response.css("div.listCon")
        sub_page_no = 1
        house_info_list = []
        for house_div in house_list_div:
            if sub_page_no > self.every_sub_page_no:
                break
            list_title_div = house_div.css("h3.listTit")[0]
            list_desc_div = house_div.css("div.listX")[0]
            house_url = list_title_div.css("a::attr(href)").extract_first()
            if not house_url:
                continue
            house_title = list_title_div.css("a::text").extract_first()
            house_publish_date_str = list_desc_div.css("p")[2].css("::text").extract_first()
            house_publish_date = house_publish_date_str.split('·')[-1].strip()[0:-2]
            house_info = {}
            house_info['house_url'] = parse.urljoin(response.url, house_url)
            house_info['house_title'] = house_title
            house_info['house_publish_date'] = house_publish_date
            house_info_list.append(house_info)
            sub_page_no += 1
        if not len(house_info_list) > 0:
            print_log_info(title='House List div is Empty, ', content=response.url)
            return

        print_log_info(title='Crawled scraped successfully from: ', content=response.url)
        yield {
            'depth': 1,
            'request_url': response.url,
            'house_info_list': house_info_list,
            'crawl_time': format_now_time()
        }

        # 下一页 分页条
        page_div = response.css("div.pageSty")
        if not page_div:
            print_log_info(title='Page div Scraped failure, ', content=response.url)
            return
        current_page_no = page_div.css("a.cur::text").extract_first()
        if int(current_page_no) >= self.total_page_no:
            print_log_info(title='Everything is over, ', content=response.url)
            return
        next_page_href = page_div.css("a.cPage::attr(href)").extract_first()
        if not next_page_href:
            print_log_info(title='Next page href is None, ', content=response.url)
            return

        time.sleep(self.every_request_delay)
        # 重要自己控制深度
        response.meta['depth'] = 1
        yield Request(url=parse.urljoin(response.url, next_page_href), callback=self.parse)


if __name__ == '__main__':
    pass
