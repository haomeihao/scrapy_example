# coding=utf-8

from scrapy import Request
from scrapy_redis import defaults
from scrapy_redis.spiders import RedisMixin, RedisSpider
from scrapy_redis.utils import bytes_to_str
from scrapy.utils.request import request_fingerprint

from scrapy_example import redis_defaults
from scrapy_example.utils import get_url_id, get_md5, print_log_info


class CustomRedisMixin(RedisMixin):

    def custom_make_request_from_url(self, url, referer, transfer_data):
        headers = {}
        if referer:
            headers['Referer'] = referer
        meta = {}
        if transfer_data:
            meta['transfer_data'] = transfer_data
        return Request(url, headers=headers, meta=meta, dont_filter=True)

    def request_seen(self, url):
        # replace request url
        new_url = url.split('?')[0]

        request = Request(url=new_url)
        fp = request_fingerprint(request)
        dupefiler_key = redis_defaults.REDIS_DUPEFILTER_KEY % {'name': self.name}
        added = self.server.sadd(dupefiler_key, fp)
        return added == 0

    def next_requests(self):
        all_url_info_key = self.settings.get('ALL_URL_INFO_KEY', redis_defaults.ALL_URL_INFO_KEY)
        all_fail_url_key = redis_defaults.ALL_FAIL_URL_KEY % {'name': self.name}
        """Returns a request to be scheduled or none."""
        use_set = self.settings.getbool('REDIS_START_URLS_AS_SET', defaults.START_URLS_AS_SET)
        fetch_one = self.server.spop if use_set else self.server.lpop
        # XXX: Do we need to use a timeout here?
        found = 0
        while found < self.redis_batch_size:
            data = fetch_one(self.redis_key)
            fail_flag = True
            if not data:
                # fail retry
                data = self.server.spop(all_fail_url_key)
                if data:
                    fail_flag = False
            if not data:
                # Queue empty.
                break

            url = bytes_to_str(data, self.redis_encoding)
            seen = self.request_seen(url)
            if seen and fail_flag:
                print_log_info(title='Request request_seen: ', content=url)
                continue

            referer = ''
            transfer_data = {}
            if all_url_info_key:
                url_id = get_url_id(url)
                if url_id:
                    all_url_info_key = all_url_info_key % {'name': self.name, 'url_id': url_id}
                    result = self.server.hgetall(all_url_info_key)
                    if result:
                        new_result = {}
                        for key, value in result.items():
                            new_result[key.decode()] = value.decode()
                        referer = new_result.get('referer', '')
                        publish_date = new_result.get('publish_date', '')
                        transfer_data = {'publish_date': publish_date}

                url_str = []
                url_str.append(url)
                url_str.append("company=0&sort=favorite&lang=0&recommend=false")
                if len(url.split("?")) > 1:
                    url = "&".join(url_str)
                else:
                    url = "?".join(url_str)

            req = self.custom_make_request_from_url(url, referer, transfer_data)
            if req:
                yield req
                found += 1
            else:
                self.logger.debug("Request not made from data: %r", data)

        if found:
            self.logger.debug("Read %s requests from '%s'", found, self.redis_key)


class CustomRedisSpider(CustomRedisMixin, RedisSpider):

    def sadd_fail_url(self, url):
        all_fail_url_key = redis_defaults.ALL_FAIL_URL_KEY % {'name': self.name}
        if not url:
            raise ValueError("url is required")
        command = "SADD " + all_fail_url_key + " " + url
        print("> " + command)
        result = self.server.sadd(all_fail_url_key, url)
        print("(integer) " + str(result))
