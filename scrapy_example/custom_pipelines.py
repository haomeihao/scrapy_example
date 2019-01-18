# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
import os

from scrapy_redis.pipelines import RedisPipeline

from scrapy_example.utils import get_second_timestamp, get_url_id, get_project_path, get_project_dir


class ScrapyExamplePipeline(object):
    def process_item(self, item, spider):
        print(item)
        spider.logger.warn(item)
        return item


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
            key = spider.name + ":all_success_url"
            data = item.get('request_url')
            self.server.sadd(key, data)
        if 'woaiwojia_list' == spider.name:
            key = spider.sub_name + ":start_urls"
            house_info_list = item.get('house_info_list')
            if len(house_info_list) > 0:
                # save list.html obtain detail.html url list
                house_url_list = [(house_info.get('house_url')) for house_info in house_info_list]
                self.server.rpush(key, *(tuple(house_url_list)))

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
                        key = spider.sub_name + ":all_url_info:" + get_url_id(house_info.get('house_url'))
                        self.server.hmset(key, data)
                end_time = get_second_timestamp()
                spider.logger.info(
                    "Redis common hmset ended, used " + str(end_time - start_time) + "seconds , " + referer)

                # use redis pipeline hmset
                start_time = get_second_timestamp()
                spider.logger.info("Redis pipeline hmset started, " + referer)
                with self.server.pipeline(transaction=False) as pipe:
                    for house_info in house_info_list:
                        data = {
                            'url': house_info.get('house_url'),
                            'referer': referer,
                            'title': house_info.get('house_title'),
                            'publish_date': house_info.get('house_publish_date')
                        }
                        if data:
                            key = spider.sub_name + ":all_url_info:" + get_url_id(house_info.get('house_url'))
                            pipe.hmset(key, data)
                    pipe.execute()
                end_time = get_second_timestamp()
                spider.logger.info(
                    "Redis pipeline hmset ended, used " + str(end_time - start_time) + "seconds , " + referer)
        if 'woaiwojia_detail' == spider.name:
            pass
        if 'init_retry' == item.get('retry_type'):
            data = item.get('retry_url', None)
            if data is not None:
                key = spider.name + ":start_urls"
                self.server.rpush(key, data)
                spider.logger.info("Init Retry Send Request to: " + data)
        return item


class JsonWithEncodingPipeline(object):
    # custom json file exporter
    def __init__(self):
        filepath = get_project_path() + '/output/data'
        filename = 'woaiwojia.json'
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        self.file = codecs.open(os.path.join(filepath, filename), 'w', encoding='utf-8')
        self.file.write('[\n')

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False)
        self.file.write(lines + ',\n')
        return item

    def spider_closed(self, spider):
        self.file.write(']')
        self.file.close()


if __name__ == '__main__':
    pass
