# coding=utf-8

"""
redis dupefilter init from all_success_url
"""

# python redis client
import redis

from scrapy import Request
# scrapy request_fingerprint
from scrapy.utils.request import request_fingerprint

from scrapy_example import redis_defaults
from scrapy_example.redis_connection_pool import pool


class RedisDupeFilterInit(object):

    def __init__(self, spider_name=None):
        # <class 'redis.client.Redis'>
        self.redis_cli = redis.Redis(connection_pool=pool)
        self.spider_name = spider_name or 'woaiwojia_detail'

    def dupefilter_init(self):
        all_success_url_key = redis_defaults.ALL_SUCCESS_URL_KEY % {'name': self.spider_name}
        dupefiler_key = redis_defaults.REDIS_DUPEFILTER_KEY % {'name': self.spider_name}

        # sscan_iter
        g = self.redis_cli.sscan_iter(all_success_url_key)
        print(type(g))
        count = self.redis_cli.scard(all_success_url_key)
        if not count > 0:
            return
        print("dupefilter set init count: " + str(count))
        for x in range(0, count):
            try:
                url = next(g).decode()
                request = Request(url=url)
                fp = request_fingerprint(request)
                added = self.redis_cli.sadd(dupefiler_key, fp)
            except Exception as e:
                print(e)
        print("dupefilter set init result: ok")


if __name__ == '__main__':
    dupefilter_init = RedisDupeFilterInit(spider_name='woaiwojia_detail')
    # dupefilter_init.dupefilter_init()
