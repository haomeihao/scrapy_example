# coding=utf-8

"""
redis seed queue init
e.g. https://bj.5i5j.com/ershoufang/
"""

# python redis client
import redis

from scrapy_example import redis_defaults
from scrapy_example.redis_connection_pool import pool


class RedisSeedInit(object):

    def __init__(self, spider_name=None):
        # <class 'redis.client.Redis'>
        self.redis_cli = redis.Redis(connection_pool=pool)
        self.spider_name = spider_name or 'woaiwojia_list'

    def print_command(self, command):
        print("> " + command)

    def print_result(self, result):
        print("(integer) " + str(result))

    def delete_dupefilter_key(self):
        dupefilter_key = redis_defaults.REDIS_DUPEFILTER_KEY % {'name': self.spider_name}

        command = "DEL " + dupefilter_key
        self.print_command(command)

        result = self.redis_cli.delete(dupefilter_key)
        self.print_result(result)

    def delete_items_key(self, items_key=''):
        if not items_key:
            items_key = redis_defaults.REDIS_ITEMS_KEY % {'name': self.spider_name}

        command = "DEL " + items_key
        self.print_command(command)

        result = self.redis_cli.delete(items_key)
        self.print_result(result)

    def push_start_urls_key(self, start_url=None):
        start_urls_key = redis_defaults.START_URLS_KEY % {'name': self.spider_name}
        start_url = start_url or 'https://bj.5i5j.com/ershoufang/'

        command = "RPUSH " + start_urls_key + " " + start_url
        self.print_command(command)

        result = self.redis_cli.rpush(start_urls_key, start_url)
        self.print_result(result)


if __name__ == '__main__':
    seed_init = RedisSeedInit(spider_name='woaiwojia_list')

    # spider_name='woaiwojia_list' need
    # seed_init.delete_dupefilter_key()
    # seed_init.delete_items_key()

    # seed_init.push_start_urls_key(start_url='https://bj.5i5j.com/ershoufang/')
