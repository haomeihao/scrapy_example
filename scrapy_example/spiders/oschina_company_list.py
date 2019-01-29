# -*- coding: utf-8 -*-
from scrapy import Request

from scrapy_redis.spiders import RedisSpider

from scrapy_example.utils import *
from scrapy_example.redis_spiders import CustomRedisSpider


class OsChinaCompanyListSpider(CustomRedisSpider):
    name = 'oschina_company_list'
    # 注意一定要写
    parent_name = ''
    sub_name = 'oschina_company_detail'

    allowed_domains = ['www.oschina.net']
    # start_urls = ['https://www.oschina.net/company']
    redis_key = name + ':start_urls'
    # RPUSH oschina_company_list:start_urls https://www.oschina.net/company

    custom_settings = {
        'DOWNLOAD_DELAY': 3
    }

    plate_name = '开源公司'

    def parse(self, response):
        # if not 200 <= response.status < 300:
        #     print_log_error(title='Response Status is Exception, ', content=log_simple_response(response))
        #     return

        # 这两行牛逼代码
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)

        container_div = response.css("div.container")
        if not container_div:
            print_log_error(title='Response Html is Wrong, ', content=log_simple_response(response))
            # push retry url
            self.sadd_fail_url(response.url)
            return

        print_log_info(title='Response Successfully, ', content=log_simple_response(response))

        company_cards = response.css("a.card")
        for company_card in company_cards:
            company_href = company_card.css("::attr(href)").extract_first()
            company_content = company_card.css("div.content")
            company_header = company_content.css("div.header::text").extract_first()
            company_desc = company_content.css("div.description::text").extract_first()

            company_os_number = company_desc.split('：')[-1].strip()

            print_log_info(title='Crawled scraped successfully from: ', content=response.url)
            yield {
                'depth': 1,
                'request_url': response.url,
                'company_url': company_href,
                'company_name': company_header,
                'company_os_number': int(company_os_number),
                'crawl_time': format_now_time()
            }


if __name__ == '__main__':
    pass
