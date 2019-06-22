# -*- coding: utf-8 -*-
from scrapy import Request

from scrapy_redis.spiders import RedisSpider

from scrapy_example.utils import *
from scrapy_example.redis_spiders import CustomRedisSpider
from urllib import parse

class GithubListCountSpider(CustomRedisSpider):
    name = 'github_list_count'
    # 注意一定要写
    parent_name = ''
    sub_name = 'github_detail'

    allowed_domains = ['github.com']
    # start_urls = ['https://github.com/']
    redis_key = name + ':start_urls'
    # RPUSH github_list:start_urls https://github.com/

    custom_settings = {
        'DOWNLOAD_DELAY': 3
    }

    plate_name = 'Github仓库'

    def parse(self, response):
        # if not 200 <= response.status < 300:
        #     print_log_error(title='Response Status is Exception, ', content=log_simple_response(response))
        #     return

        # 这两行牛逼代码
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)

        container_div = response.css("div.codesearch-results")
        if not container_div:
            print_log_error(title='Response Html is Wrong, ', content=log_simple_response(response))
            # push retry url
            self.sadd_fail_url(response.url)
            return

        print_log_info(title='Response Successfully, ', content=log_simple_response(response))

        url_prefix = 'https://github.com'
        stars_limit_start = response.request.url.find('%3E')+len('%3E')
        stars_limit_end = response.request.url.find('+')
        stars_limit = response.request.url[stars_limit_start:stars_limit_end]
        repo_language = response.request.url.split('language%3A')[-1]
        repo_language = repo_language.split('&')[0]
        repo_language = parse.unquote(repo_language)

        language_count = response.css(".flex-justify-between")[-1].css("h3::text").extract_first()
        if language_count:
            language_count = language_count.replace('\n', '').strip()
            language_count = language_count.split(' ')[0]
        else:
            language_count = '0'
            print('repo_language: {}, language_count: {}', repo_language, language_count)

        yield {
            'depth': 0,
            'request_url': response.request.url,
            'stars_limit': int(stars_limit),
            'repo_language': repo_language,
            'language_count': int(language_count),
            'crawl_time': format_now_time()
        }


if __name__ == '__main__':
    pass
