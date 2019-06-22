# -*- coding: utf-8 -*-
from scrapy import Request

from scrapy_redis.spiders import RedisSpider

from scrapy_example.utils import *
from scrapy_example.redis_spiders import CustomRedisSpider

from scrapy_example.websocket_example import WebSocketClient


class MfcclubIndexSpider(CustomRedisSpider):
    name = 'mfcclub_index'
    # 注意一定要写
    parent_name = ''
    sub_name = ''

    allowed_domains = ['www.mfcclub.com']
    # start_urls = ['https://https://www.mfcclub.com/login.jsp?locale=zh_CN']
    redis_key = name + ':start_urls'
    # RPUSH oschina_company_list:start_urls https://www.mfcclub.com/login.jsp?locale=zh_CN#
    # RPUSH oschina_company_list:start_urls https://www.mfcclub.info/login.jsp
    # RPUSH oschina_company_list:start_urls https://www.mfcclub.net/login.jsp?locale=zh_CN
    # RPUSH oschina_company_list:start_urls https://www.mfcteam.info/login.jsp
    # RPUSH oschina_company_list:start_urls https://www.mfcteam.com/login.jsp

    custom_settings = {
        'DOWNLOAD_DELAY': 3
    }

    plate_name = 'MFC首页'

    def send_msg(self, msg="有新通知"):
        try:
            client = WebSocketClient()
            client.send_msg(msg)
            print("发送WebSocket消息: ", msg)
        except Exception as e:
            print("WebSocket发生异常: ", e)

    def parse(self, response):
        # if not 200 <= response.status < 300:
        #     print_log_error(title='Response Status is Exception, ', content=log_simple_response(response))
        #     return

        # 这两行牛逼代码
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)

        form_div = response.css(".stdform")
        if not form_div:
            print_log_error(title='Response Html is Wrong, ', content=log_simple_response(response))
            # push retry url
            self.sadd_fail_url(response.url)
            return

        print_log_info(title='Response Successfully, ', content=log_simple_response(response))

        self.send_msg(msg="[" + response.url + "]页面可以正常访问了")


if __name__ == '__main__':
    pass
