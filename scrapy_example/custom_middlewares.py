# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import random
from scrapy import signals
from scrapy import Request
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.exceptions import NotConfigured
from scrapy.spidermiddlewares.httperror import HttpErrorMiddleware
from scrapy.utils.project import get_project_settings
from scrapy.utils.python import to_native_str
from scrapy.utils.response import response_status_message

from scrapy_example.utils import *

settings = get_project_settings()


# from fake_useragent import UserAgent


# Scrapy Spider Example
# to Custom Spider
class ScrapyExampleSpiderMiddleware(object):

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # downloader process_response 之后跳到这里
        # 此时的 response.request为{Request} response.meta为{dict}
        # 此步骤是 process_spider_output yield 之内的
        # response.headers{Headers}里有 Set-Cookie, X-Via 等信息
        # response.meta里有 depth 信息
        # request.headers{Request}里有 Referer, User-Agent, Cookie 等信息

        # 此函数为处理响应状态或信息
        # print("响应 后置处理 (2), " + log_simple_response(response))
        return None

    def process_spider_output(self, response, result, spider):
        # 此函数用于对响应匹配到的url集合 发出一系列新请求
        # print("响应 后置处理 (3), " + log_simple_response(response))
        for i in result:
            # 因为此时一些信息没构造完，调用打印会抛异常
            # AttributeError: 'dict' object has no attribute 'method'
            # print("响应.请求 后置处理 (三), " + log_simple_request(i))
            yield i

    def process_spider_exception(self, response, exception, spider):
        pass

    def process_start_requests(self, start_requests, spider):
        for r in start_requests:
            # print("请求 前置处理 (1), " + log_simple_request(r))
            yield r

    def spider_opened(self, spider):
        spider.logger.info('ScrapyExampleSpiderMiddleware Spider opened: %s' % spider.name)


class CustomHttpErrorSpiderMiddleware(ScrapyExampleSpiderMiddleware):

    def process_spider_input(self, response, spider):
        spider.logger.info("SpiderMiddleware process_spider_input, " + log_simple_response(response))

        # common case
        if 200 <= response.status < 300:
            spider.logger.info(log_response(response))
        else:
            spider.logger.error(log_response(response))

        # 应在此处理 403 异常 重试
        # if 403 == response.status:  # common case
        # print_log_error(title='Response 403 Retry, ', content=log_simple_response(response))
        # AssertionError: Middleware CustomHttpErrorSpiderMiddleware.process_spider_input must returns None or raise an exception, got <class 'generator'>
        # 看来不能在此处 yield 请求
        # yield Request(url=response.url)
        # pass
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
        # class scrapy.http.Request(url[, callback, method='GET', headers, body,
        # cookies, meta, encoding='utf-8', priority=0, dont_filter=False, errback, flags])
        pass

    def process_response(self, request, response, spider):
        # class scrapy.http.Response(url[, status=200, headers=None, body=b'', flags=None, request=None])
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

        # 每次请求 dont_merge_cookies 为 False
        # 为True时就禁用了cookie传递 用做处理403的问题，重发请求带此参数
        # request.meta['dont_merge_cookies'] = True
        # 一个 参数 解决临时一个请求的cookie传递问题

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
            # request.headers['Cookie'] = None
            # spider.logger.info("not None Cookie set None, " + log_simple_request(request))
            # 如此一来 响应那里就不用处理了
            # 处理思路: 请求防止403 以及响应403重试
            # 这里是处理防止403 应在 spidermiddleware 里处理响应403重试
            # request.meta['dont_merge_cookies'] = True
            spider.logger.info("Set request.meta.dont_merge_cookies True, " + log_simple_request(request))

    def spider_opened(self, spider):
        spider.logger.info('UserAgentDownloaderMiddleware Spider opened: %s' % spider.name)


class CookieDownloaderMiddleware(ScrapyExampleDownloaderMiddleware):

    def process_request(self, request, spider):
        # print("请求 前置处理 (2) , " + log_simple_request(request))
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
        # 此时 response.request为NoneType(None) response.meta为str 不规范的一串字符
        # res_headers = parse_to_dict(response.headers)
        # set_cookie = res_headers.get('Set-Cookie')  # str type
        byte_set_cookie_list = response.headers.getlist('Set-Cookie')  # have b'
        # 处理 set-cookie 防止 403
        str_set_cookie_list = [to_native_str(c, errors='replace') for c in byte_set_cookie_list]
        filer_index, new_cookie = self.get_filter_index(str_set_cookie_list)
        # 第一种处理 自己设置响应的 Set-Cookie 还是有 403 证明不正确
        # byte_set_cookie_list.pop(filer_index)
        # byte_set_cookie_list.append(new_cookie.encode())
        # byte_set_cookie_list.append(new_cookie)
        # response.headers['Set-Cookie'] = byte_set_cookie_list

        # 第二种处理 直接把 Set-Cookie 全部清空 让目标服务器自动处理
        # 这样虽然暂时没有 403 ，但是 请求时还是会发送 cookiejar 里的 cookie
        # 可以尝试 在发送请求之前 加一次 cookie 的处理
        # 发送请求之前 加了 cookie 处理 还是会发送 cookie 必须处理 cookiejar 里的 cookie
        # 请求前置处理 dont_merge_cookies 为 True 这里上次响应无需处理 只需处理403重试即可
        if filer_index is not None:
            response.headers['Set-Cookie'] = None
            spider.logger.info("Handle Set-Cookie to prevent 403 Exception, " + log_simple_response(response))

        # spider.logger.info("Want but not Handle Set-Cookie to prevent 403 Exception, " + log_simple_response(response))

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
            if response.status == 403:
                # request.meta['dont_merge_cookies'] = True
                spider.logger.error("Response 403 Retry, " + log_simple_response(response))
                spider.logger.error("403 Retry Set dont_merge_cookies True, " + log_simple_request(request))
            return self._retry(request, reason, spider) or response
        return response

# 第三方库 fake_useragent 随机更换 user-agent
# class RandomUserAgentMiddleware(object):
#     def __init__(self, crawler):
#         self.ua = UserAgent()
#         self.ua_type = crawler.settings.get('RANDOM_UA_TYPE', 'random')
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         return cls(crawler)
#
#     def process_request(self, request, spider):
#         def get_ua():
#             return getattr(self.ua, self.ua_type)
#
#         random_ua = get_ua()
#         request.headers.setdefault('User-Agent', random_ua)
