# coding=utf-8

# python redis client
import redis

from scrapy.utils.project import get_project_settings

# global settings
settings = get_project_settings()

host = settings.get('REDIS_HOST')
port = settings.getint('REDIS_PORT')
# <class 'redis.connection.ConnectionPool'>
pool = redis.ConnectionPool(host=host, port=port, db=0)
