# coding=utf-8

# For standalone use.
DUPEFILTER_KEY = 'dupefilter:%(timestamp)s'

PIPELINE_KEY = '%(spider)s:items'

SCHEDULER_QUEUE_KEY = '%(spider)s:requests'
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.PriorityQueue'
SCHEDULER_DUPEFILTER_KEY = '%(spider)s:dupefilter'
SCHEDULER_DUPEFILTER_CLASS = 'scrapy_redis.dupefilter.RFPDupeFilter'

START_URLS_KEY = '%(name)s:start_urls'
START_URLS_AS_SET = False

# Custom
ALL_URL_INFO_KEY = '%(name)s:all_url_info:%(url_id)s'
ALL_SUCCESS_URL_KEY = '%(name)s:all_success_url'
ALL_FAIL_URL_KEY = '%(name)s:all_fail_url'
# Custom
REDIS_DUPEFILTER_KEY = '%(name)s:dupefilter'
REDIS_ITEMS_KEY = '%(name)s:items'
REDIS_REPLICA_KEY = '%(name)s:replica'
REDIS_HOSTNAME_PID_COUNTER_KEY = '%(name)s:counter:%(hostname)s:%(pid)s'
REDIS_ZSET_KEY = '%(name)s:zset'
# for dev redis keys no permission
REDIS_COUNTER_KEY_SET_KEY = '%(name)s:counter_key_set'
