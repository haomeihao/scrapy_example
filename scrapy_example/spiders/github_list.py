# -*- coding: utf-8 -*-
from scrapy import Request

from scrapy_redis.spiders import RedisSpider

from scrapy_example.utils import *
from scrapy_example.redis_spiders import CustomRedisSpider


class GithubListSpider(CustomRedisSpider):
    name = 'github_list'
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
        repo_language = response.request.url.split('language%3A')[-1]
        repo_language = repo_language.split('&')[0]
        result_count = response.css(".flex-justify-between")[-1].css("h3::text").extract_first()
        result_count = result_count.replace('\n', '').strip()
        result_count = result_count.split(' ')[0]
        repo_list = response.css("ul.repo-list li.repo-list-item")
        length = len(repo_list)
        for i in range(length-1):
            repo = repo_list[i]
            repo_name = repo.css("a::text").extract_first()
            repo_href = repo.css("a::attr(href)").extract_first()
            repo_stars = repo.css('.muted-link::text')[-1].extract()
            repo_stars = repo_stars.replace('\n', '').strip()
            # if repo_stars.find('k') != -1:
            #     repo_stars_parse = float(repo_stars[0:-1]) * 1000
            # else:
            #     repo_stars_parse = float(repo_stars)

            print_log_info(title='Crawled scraped successfully from: ', content=response.url)
            yield {
                'depth': 1,
                'request_url': response.request.url,
                'repo_language': repo_language,
                'result_count': result_count,
                'repo_name': repo_name,
                'repo_href': url_prefix + repo_href,
                'repo_stars': repo_stars,
                # 'repo_stars_parse': repo_stars_parse,
                'crawl_time': format_now_time()
            }


if __name__ == '__main__':
    pass
