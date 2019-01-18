# -*- coding: utf-8 -*-
from scrapy import Request

from scrapy_redis.spiders import RedisSpider

from scrapy_example.utils import *
from scrapy_example.redis_spiders import CustomRedisSpider


class WoaiwojiaSpider(CustomRedisSpider):
    name = 'woaiwojia_detail'
    # 注意一定要写
    parent_name = 'woaiwojia_list'
    sub_name = ''

    allowed_domains = ['bj.5i5j.com']
    # start_urls = ['https://bj.5i5j.com/ershoufang/']
    redis_key = name + ':start_urls'
    # RPUSH woaiwojia_detail:start_urls https://bj.5i5j.com/ershoufang/xxx.html

    custom_settings = {
        'DOWNLOAD_DELAY': 3
    }

    plate_name = '二手房'

    def parse(self, response):
        # if not 200 <= response.status < 300:
        #     print_log_error(title='Response Status is Exception, ', content=log_simple_response(response))
        #     return

        house_title_div = response.css("div.rent-top")
        if not house_title_div:
            print_log_error(title='Response Html is Wrong, ', content=log_simple_response(response))

            custom_meta = {}
            transfer_data = response.meta.get('transfer_data')
            if transfer_data:
                custom_meta['transfer_data'] = transfer_data
            # push retry url
            self.sadd_fail_url(response.url)
            # yield Request(url=response.url, callback=self.parse, meta=custom_meta)
            return

        print_log_info(title='Response Successfully, ', content=log_simple_response(response))

        house_title = house_title_div.css("h1.house-tit::text")
        if not house_title:
            print_log_info(title='House Title div Scraped failure, ', content=response.url)
            return
        house_title = house_title.extract_first().strip()
        house_desc = house_title_div.css("p::text").extract_first().strip()
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

        house_publish_date = ''
        transfer_data = response.meta.get('transfer_data')
        if transfer_data:
            house_publish_date = transfer_data.get('publish_date')

        print_log_info(title='Crawled scraped successfully from: ', content=response.url)
        yield {
            'depth': 2,
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
        }


if __name__ == '__main__':
    pass
