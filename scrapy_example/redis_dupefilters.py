# coding=utf-8
from scrapy_redis.dupefilter import RFPDupeFilter as RedisSetDupeFilter
from scrapy_redis_bloomfilter.dupefilter import RFPDupeFilter as BloomFilterDupeFilter


class CustomRedisSetDupeFilter(RedisSetDupeFilter):

    def request_seen(self, request):
        # replace request url
        origin_url = request.url
        new_url = origin_url.split('?')[0]
        request = request.replace(url=new_url)

        fp = self.request_fingerprint(request)
        # custom dupe filter
        # default crawl urls not crawl successfully urls
        # init a set/bloomfilter data set
        added = self.server.sadd(self.key, fp)
        return added == 0


class CustomBloomFilterDupeFilter(BloomFilterDupeFilter):

    def request_seen(self, request):
        # replace request url
        origin_url = request.url
        new_url = origin_url.split('?')[0]
        request = request.replace(url=new_url)

        fp = self.request_fingerprint(request)
        if self.bf.exists(fp):
            return True
        self.bf.insert(fp)
        return False
