# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import random

import redis
from scrapy import signals
from scrapy.downloadermiddlewares.cookies import CookiesMiddleware
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.exceptions import NotConfigured
from scrapy.utils.project import get_project_settings
from scrapy.utils.python import to_native_str
from scrapy.utils.response import response_status_message

from scrapy_example import redis_defaults
from scrapy_example.utils import *
from scrapy_example.redis_connection_pool import pool

settings = get_project_settings()


# Scrapy Spider Example
# to Custom Spider
class ScrapyExampleSpiderMiddleware(object):

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        return None

    def process_spider_output(self, response, result, spider):
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        pass

    def process_start_requests(self, start_requests, spider):
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('ScrapyExampleSpiderMiddleware Spider opened: %s' % spider.name)


class CustomHttpErrorSpiderMiddleware(ScrapyExampleSpiderMiddleware):

    def __init__(self, spider):
        self.redis_cli = redis.Redis(connection_pool=pool)
        self.all_fail_url_key = redis_defaults.ALL_FAIL_URL_KEY % {'name': spider.name}

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.spider:
            return
        s = cls(crawler.spider)
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        spider.logger.info("SpiderMiddleware process_spider_input, " + log_simple_response(response))
        if 200 <= response.status < 300:
            spider.logger.info(log_response(response))
        else:
            spider.logger.error(log_response(response))
            fail_status_list = [403, 504]
            if response.status in fail_status_list:
                self.redis_cli.sadd(self.all_fail_url_key, response.url)
        return None

    def process_spider_output(self, response, result, spider):
        for i in result:
            yield i

    def spider_opened(self, spider):
        spider.logger.info('CustomHttpErrorSpiderMiddleware Spider opened: %s' % spider.name)


# Scrapy Downloader Example
# to Scrapy Downloader
class ScrapyExampleDownloaderMiddleware(object):

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        pass

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        pass

    def spider_opened(self, spider):
        spider.logger.info('ScrapyExampleDownloaderMiddleware Spider opened: %s' % spider.name)


# 随机切换 ip proxy
class ProxyDownloaderMiddleware(ScrapyExampleDownloaderMiddleware):

    def process_request(self, request, spider):
        # 每次请求都随机切换 proxy
        proxy = request.meta.get('proxy', None)
        if proxy is None:
            proxy_list = settings.getlist('PROXY_LIST')
            proxy = random.choice(proxy_list)
            request.meta['proxy'] = proxy
            spider.logger.info("None proxy set random proxy, " + log_simple_request(request))

    def spider_opened(self, spider):
        spider.logger.info('ProxyDownloaderMiddleware Spider opened: %s' % spider.name)


# 随机切换 user-agent
class UserAgentDownloaderMiddleware(ScrapyExampleDownloaderMiddleware):

    def is_dont_merge_cookies(self, set_cookie_list):
        flag = False
        cookie_name = 'ershoufang_BROWSES'
        split_str = '%2C'
        for index, item in enumerate(set_cookie_list):
            item_list = item.split(';')
            key_value = item_list[0]
            if not key_value.startswith(cookie_name):
                continue
            value = key_value.split('=')[-1]
            value_len = len(value.split(split_str))
            if not value_len > 10:
                break
            flag = True
            break
        return flag

    def process_request(self, request, spider):
        # 第一次请求随机切换 user-agent
        user_agent = request.headers.get('User-Agent', None)
        if user_agent is None:
            user_agent_list = settings.get('USER_AGENT_LIST', [])
            user_agent = random.choice(user_agent_list)
            request.headers['User-Agent'] = user_agent
            spider.logger.info("None User-Agent set random User-Agent, " + log_simple_request(request))

        # 一起在此 Downloader 处理 request.headers.Referer
        referer = request.headers.get('Referer', None)
        if referer is None:
            random_int = random.randint(0, 9)
            referer = 'https://bj.5i5j.com/ershoufang/n' + str(random_int) + '/'
            request.headers['Referer'] = referer
            spider.logger.info("None Referer set random Referer, " + log_simple_request(request))

        # 默认 cookie 处理器 的 请求前置处理
        dont_merge_cookies = request.meta.get('dont_merge_cookies', False)
        # 如果本来就是 True 就不处理
        if dont_merge_cookies:
            return
        byte_set_cookie_list = request.headers.getlist('Cookie')  # have b'
        str_set_cookie_list = [to_native_str(c, errors='replace') for c in byte_set_cookie_list]
        # 处理 cookie 防止 403
        dont_merge_cookies = self.is_dont_merge_cookies(str_set_cookie_list)
        spider.logger.info(
            "Judge is_dont_merge_cookies: " + str(dont_merge_cookies) + ", " + log_simple_request(request))
        if dont_merge_cookies:
            request.headers['Cookie'] = None
            request.meta['dont_merge_cookies'] = True
            spider.logger.info("Set request.meta.dont_merge_cookies True, " + log_simple_request(request))

    def spider_opened(self, spider):
        spider.logger.info('UserAgentDownloaderMiddleware Spider opened: %s' % spider.name)


class CookieDownloaderMiddleware(ScrapyExampleDownloaderMiddleware):

    def process_request(self, request, spider):
        spider.logger.info(log_request(request))

    def get_filter_index(self, set_cookie_list):
        filer_index = None
        new_cookie = ''
        cookie_name = 'ershoufang_BROWSES'
        split_str = '%2C'
        for index, item in enumerate(set_cookie_list):
            item_list = item.split(';')
            key_value = item_list[0]
            if not key_value.startswith(cookie_name):
                continue
            value = key_value.split('=')[-1]
            value_len = len(value.split(split_str))
            if not value_len > 10:
                break
            filer_index = index
            sub_value = value.split(split_str)[-1]
            item_list[0] = '='.join([cookie_name, sub_value])
            new_cookie = ';'.join(item_list)
            break
        return filer_index, new_cookie

    def process_response(self, request, response, spider):
        # replace response url
        origin_url = response.url
        new_url = origin_url.split('?')[0]
        response = response.replace(url=new_url)

        byte_set_cookie_list = response.headers.getlist('Set-Cookie')  # have b'
        # 处理 set-cookie 防止 403
        str_set_cookie_list = [to_native_str(c, errors='replace') for c in byte_set_cookie_list]
        filer_index, new_cookie = self.get_filter_index(str_set_cookie_list)
        if filer_index is not None:
            response.headers['Set-Cookie'] = None
            spider.logger.info("Handle Set-Cookie to prevent 403 Exception, " + log_simple_response(response))

        return response

    def spider_opened(self, spider):
        spider.logger.info('CookieDownloaderMiddleware Spider opened: %s' % spider.name)


class RetryDownloaderMiddleware(RetryMiddleware):

    def __init__(self, settings):
        super().__init__(settings)
        if not settings.getbool('HTTPERROR_RETRY_ENABLED'):
            raise NotConfigured
        self.max_retry_times = settings.getint('HTTPERROR_RETRY_TIMES')
        self.retry_http_codes = set(int(x) for x in settings.getlist('HTTPERROR_RETRY_CODES'))
        self.priority_adjust = settings.getint('HTTPERROR_RETRY_PRIORITY_ADJUST')

    def process_response(self, request, response, spider):
        if request.meta.get('dont_retry', False):
            return response
        if response.status in self.retry_http_codes:
            reason = response_status_message(response.status)
            body = response.text
            body_len = len(body)
            if body_len < 300:
                if isinstance(body, bytes):
                    body = body.decode()
                url = pattern_url(body)
                if url:
                    print_log_error(title='pattern script url: ', content=url)
                    # request.headers['Cookie'] = None
                    request = request.replace(url=url)
            if response.status == 403:
                request.headers['Cookie'] = None
                spider.logger.error("Response 403 Retry, " + log_simple_response(response))
            return self._retry(request, reason, spider) or response
        return response

    def spider_opened(self, spider):
        spider.logger.info('RetryDownloaderMiddleware Spider opened: %s' % spider.name)


class CookieJarDownloaderMiddleware(CookiesMiddleware):

    def process_response(self, request, response, spider):
        if request.meta.get('dont_merge_cookies', False):
            return response

        # extract cookies from Set-Cookie and drop invalid/expired cookies
        cookiejarkey = request.meta.get("cookiejar")
        jar = self.jars[cookiejarkey]

        if response.status == 403:
            # if "woaiwojia_list" == spider.name:
            jar.clear()
            jar.clear_session_cookies()
            spider.logger.error("Response 403 clear cookiejar, " + log_simple_response(response))

        jar.extract_cookies(response, request)
        self._debug_set_cookie(response, spider)

        return response

    def spider_opened(self, spider):
        spider.logger.info('CookieJarDownloaderMiddleware Spider opened: %s' % spider.name)
