# -*- coding: utf-8 -*-
from scrapy import Request

from scrapy_redis.spiders import RedisSpider

from scrapy_example.utils import *
from scrapy_example.redis_spiders import CustomRedisSpider


class OsChinaCompanyDetailSpider(CustomRedisSpider):
    name = 'oschina_company_detail'
    # 注意一定要写
    parent_name = 'oschina_company_list'
    sub_name = ''

    allowed_domains = ['www.oschina.net']
    # start_urls = ['https://www.oschina.net/project/apache']
    redis_key = name + ':start_urls'
    # RPUSH oschina_company_detail:start_urls https://www.oschina.net/project/apache

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

        container_div = response.css("div.projects-list-container")
        if not container_div:
            print_log_error(title='Response Html is Wrong, ', content=log_simple_response(response))
            # push retry url
            self.sadd_fail_url(response.url)
            return

        print_log_info(title='Response Successfully, ', content=log_simple_response(response))

        project_items = response.css("div.project-item")
        for project_item in project_items:
            content_div = project_item.css("div.content")

            header_div = content_div.css("h3.header")
            project_url = header_div.css("a::attr(href)").extract_first()
            project_name = header_div.css("span.project-name::text").extract_first()
            project_title = header_div.css("span.project-title::text").extract_first()

            if not project_name or not project_url:
                return

            extra_div = content_div.css("div.extra")
            extra_items = extra_div.css("div.item")

            collect_count = '0'
            comment_count = '0'
            update_time = ''

            if len(extra_items) > 0:
                extra_item_collect = extra_items[0].css("::text").extract_first()
                collect_count = extra_item_collect.split(' ')[-1].strip()
                if not collect_count: collect_count = '0'
            if len(extra_items) > 1:
                extra_item_comment = extra_items[1].css("a::text").extract_first()
                comment_count = extra_item_comment.split(' ')[-1].strip()
                if not comment_count: comment_count = '0'
            if len(extra_items) > 2:
                extra_item_update_time = extra_items[2].css("::text").extract_first()
                update_time = extra_item_update_time.split(' ')[-1].strip()

            print_log_info(title='Crawled scraped successfully from: ', content=response.url)
            yield {
                'depth': 1,
                'request_url': response.url,
                'project_url': project_url,
                'project_name': project_name,
                'project_title': project_title,
                'collect_count': int(collect_count),
                'comment_count': int(comment_count),
                'update_time': update_time,
                'crawl_time': format_now_time()
            }


if __name__ == '__main__':
    pass
