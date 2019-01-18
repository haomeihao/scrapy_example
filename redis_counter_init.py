# coding=utf-8

import os
import socket
import redis
from scrapy_example.redis_connection_pool import pool
from scrapy_example import redis_defaults


class RedisCounterInit(object):

    def __init__(self, spider_name):
        self.redis_cli = redis.Redis(connection_pool=pool)
        self.key = redis_defaults.REDIS_HOSTNAME_PID_COUNTER_KEY
        self.key_set = redis_defaults.REDIS_COUNTER_KEY_SET_KEY
        if not spider_name:
            raise ValueError("spider_name is required")
        self.spider_name = spider_name

    def init(self):
        # key = "woaiwojia_detail:counter:PAFSH-L2013:11986"
        key = self.key % {'name': self.spider_name, 'hostname': socket.gethostname(), 'pid': str(os.getpid())}
        # result = self.redis_cli.getset(key, 0)
        # if result and isinstance(result, bytes):
        #     result = result.decode()
        # print(key + " init result: " + str(result))

        key_set = self.key_set % {'name': self.spider_name}
        result = self.redis_cli.sadd(key_set, key)
        if result and isinstance(result, bytes):
            result = result.decode()
        print(key + " sadd key result: " + str(result))

    def incr(self):
        # key = "woaiwojia_detail:counter:PAFSH-L2013:11986"
        key = self.key % {'name': self.spider_name, 'hostname': socket.gethostname(), 'pid': str(os.getpid())}
        # init
        self.redis_cli.setnx(key, 0)
        # if not result:
            # raise ValueError("key is not exist")
        result = self.redis_cli.incr(key)
        print(key + " incr result: " + str(result))

    def clear(self):
        pattern = self.key % {'name': self.spider_name, 'hostname': socket.gethostname(), 'pid': '*'}
        result = self.redis_cli.keys(pattern)
        print(pattern + " pattern keys len: " + str(len(result)))
        for item in result:
            if isinstance(item, bytes):
                item = item.decode()
            result = self.redis_cli.get(item)
            if isinstance(result, bytes):
                result = result.decode()
            # if int(result) > 0:
            #     continue
            self.redis_cli.delete(item)
        print(pattern + " pattern keys clear ok")

    def not_keys_clear(self):
        key_set = self.key_set % {'name': self.spider_name}
        g = self.redis_cli.sscan_iter(key_set)
        print(type(g))
        count = self.redis_cli.scard(key_set)
        if not count > 0:
            return
        print("counter key set count: " + str(count))
        for x in range(0, count):
            try:
                counter_key = next(g).decode()
                self.redis_cli.delete(counter_key)
            except Exception as e:
                print(e)
        print("delete counter by key set result: ok")
        self.redis_cli.delete(key_set)
        print("delete counter key set result: ok")


if __name__ == '__main__':
    counter_init = RedisCounterInit(spider_name='woaiwojia_list')
    counter_init.clear()
    # counter_init.init()
    # counter_init.incr()

    counter_init2 = RedisCounterInit(spider_name='woaiwojia_detail')
    counter_init2.clear()
