# coding=utf-8

# Current Version 3.0.1
import json

import redis
from scrapy.utils.python import to_native_str


def process_decode(data):
    def inner_func(item):
        if isinstance(item, bytes):
            return item.decode()
        elif isinstance(item, tuple):
            return tuple(inner_func(ele) for ele in item)
        else:
            return item

    if isinstance(data, list):
        return list(inner_func(item) for item in data)
    else:
        return inner_func(data)


# Getting Started
# r = redis.Redis(host='127.0.0.1', port=6378)
# r.set('foo', 'bar')
# result = r.get('foo')
# print(process_decode(result))

# Client Classes: Redis and StrictRedis

# Connection Pools
redis_pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0)
redis_cli = redis.Redis(connection_pool=redis_pool)


# result = r.hgetall('woaiwojia_detail:all_url_info:37193176')

# new_result = {}
# for key, value in result.items():
#     new_result[key.decode()] = value.decode()
# for key, value in new_result.items():
#     print(key, '=', value)

# key = "test:dupefilter"
# for x in range(0, 100):
#     r.sadd(key, x)
# Pipelines
# r.set('bing', 'baz')
# pipe = r.pipeline()
# pipe.set('foo', 'bar')
# pipe.get('bing')
# result = pipe.execute()
#
# print([process_decode(item) for item in result])

# result = pipe.set('foo', 'bar').sadd('faz', 'baz').incr('auto_number').execute()
# print([process_decode(item) for item in result])

# with r.pipeline(transaction=False) as pipe:
#     def sadd(data):
#         pipe.hmset(key + str(data), data)
#
#
#     key = "test:all_url_info:"
#     [sadd(data) for data in range(1, 11)]
#     result = pipe.execute()

# zset
# r.zincrby("myzset", 1, "one")
# r.zincrby("myzset", 1, "two")
# r.zincrby("myzset", 1, "three")
# r.zincrby("myzset", 1, "two")
# r.zincrby("myzset", 1, "three")
# r.zincrby("myzset", 1, "two")

# result = r.zrangebyscore(name="myzset", min=0, max=1 << 31, start=0, num=10, withscores=True)
# [print(process_decode(item)) for item in result]

def tuple_to_dict(tuple_data):
    return {"language": tuple_data[0], "count": int(tuple_data[1])}


def page_result(stars):
    total_result = []
    print('Github各大语言stars>{0}仓库数量排行榜'.format(str(stars)))
    key = 'github_list_count:%(stars)s' % {'stars': str(stars)}
    limit = 30
    for index in range(0, 3):
        offset = index * limit
        rev_result = redis_cli.zrevrangebyscore(name=key, min=0, max=1 << 31, start=offset, num=limit, withscores=True)
        final_result = [(tuple_to_dict(process_decode(item))) for item in rev_result]
        final_result = [result for result in final_result if result['count'] > 0]
        if len(final_result) > 0:
            total_result.extend(final_result)
            [print(item) for item in final_result]
            print("-" * 24 + " 第 " + str(index + 1) + " 页 " + "-" * 24)

    return total_result


def parse_github_result():
    key = 'github_list_count:items'
    length = redis_cli.llen(key)
    for item in redis_cli.lrange(key, 0, length - 1):
        info = json.loads(to_native_str(item))
        stars = info['stars_limit']
        language = info['repo_language']
        count = info['language_count']
        zset_key = 'github_list_count:%(stars)s' % {'stars': str(stars)}
        print(zset_key, stars, language, count)
        redis_cli.zincrby(zset_key, count, language)


if __name__ == '__main__':
    # parse_github_result()
    for stars in [30000, 10000]:
        page_result(stars)