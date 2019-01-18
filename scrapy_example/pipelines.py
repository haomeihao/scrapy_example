# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import os
import socket

from scrapy.utils.project import get_project_settings

settings = get_project_settings()

from scrapy_redis import defaults
from scrapy_redis.pipelines import RedisPipeline

from scrapy_example.utils import get_second_timestamp, get_url_id, format_now_time
from scrapy_example import redis_defaults


class ScrapyExamplePipeline(object):
    def process_item(self, item, spider):
        new_item = {}
        new_item['hostname'] = socket.gethostname()
        new_item['host'] = socket.gethostbyname(socket.gethostname())
        new_item['pid'] = os.getpid()
        new_item['crawl_time'] = format_now_time()
        new_item.update(item)
        print(new_item)
        spider.logger.warn(new_item)
        return new_item


class CustomRedisPipeline(RedisPipeline):

    def _process_item(self, item, spider):
        # common save logic
        if spider.name is not None:
            # use list save items
            key = self.item_key(item, spider)
            # data = self.serialize(item)
            data = json.dumps(item, ensure_ascii=False)
            self.server.rpush(key, data)

            # use set save crawl successfully url
            all_success_url_key = redis_defaults.ALL_SUCCESS_URL_KEY % {'name': spider.name}
            data = item.get('request_url')
            self.server.sadd(all_success_url_key, data)

            # counter
            counter_key = redis_defaults.REDIS_HOSTNAME_PID_COUNTER_KEY
            counter_key = counter_key % {'name': spider.name, 'hostname': socket.gethostname(), 'pid': str(os.getpid())}
            result = self.server.incr(counter_key)
        if 'woaiwojia_list' == spider.name:
            start_urls_key = redis_defaults.START_URLS_KEY % {'name': spider.sub_name}
            house_info_list = item.get('house_info_list')
            if len(house_info_list) > 0:
                # save list.html obtain detail.html url list
                house_url_list = [(house_info.get('house_url')) for house_info in house_info_list]
                use_set = settings.getbool('REDIS_START_URLS_AS_SET', defaults.START_URLS_AS_SET)
                add_one = self.server.sadd if use_set else self.server.rpush
                add_one(start_urls_key, *(tuple(house_url_list)))

                # save som about url info to use transfer or query
                referer = item.get('request_url')

                # use redis common hmset
                start_time = get_second_timestamp()
                spider.logger.info("Redis common hmset started, " + referer)
                for house_info in house_info_list:
                    data = {
                        'url': house_info.get('house_url'),
                        'referer': referer,
                        'title': house_info.get('house_title'),
                        'publish_date': house_info.get('house_publish_date')
                    }
                    if data:
                        url_id = get_url_id(house_info.get('house_url'))
                        all_url_info_key = redis_defaults.ALL_URL_INFO_KEY % {'name': spider.sub_name, 'url_id': url_id}
                        self.server.hmset(all_url_info_key, data)
                end_time = get_second_timestamp()
                spider.logger.info(
                    "Redis common hmset ended, used " + str(end_time - start_time) + "seconds , " + referer)
        if 'woaiwojia_detail' == spider.name:
            pass
        if 'init_retry' == item.get('retry_type'):
            data = item.get('retry_url', None)
            if data is not None:
                key = redis_defaults.START_URLS_KEY % {'name': spider.name}
                self.server.rpush(key, data)
                spider.logger.info("Init Retry Send Request to: " + data)

        return item


if __name__ == '__main__':
    pass
