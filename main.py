# coding=utf-8

import sys
import os
from scrapy.cmdline import execute

from redis_counter_init import RedisCounterInit
from redis_dupefilter_init import RedisDupeFilterInit
from redis_seed_init import RedisSeedInit
from scrapy_example.utils import before_main_create_dir, before_main_remove_file

# 注意这行代码必须加上 否则配置的输出文件路径有问题
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# only modify this spider_name & start_url is ok
# spider_name = 'woaiwojia_list'
# start_url = 'https://bj.5i5j.com/ershoufang/'
# spider_name = 'oschina_company_list'
# start_url = 'https://www.oschina.net/company'
spider_name = 'github_list'
start_url = 'https://github.com/search?q=stars%3A>30000+language%3Ajava'

# 1. before main create directory folder
before_main_create_dir(spider_name=spider_name)

# 2. init a counter
counter_init = RedisCounterInit(spider_name=spider_name)
counter_init.init()

# 3. woaiwojia_detail dupefilter init
# dupefilter_init = RedisDupeFilterInit(spider_name='woaiwojia_detail')
# dupefilter_init.dupefilter_init()

# 4. woaiwojia_list start_urls init
seed_init = RedisSeedInit(spider_name=spider_name)
# spider_name='woaiwojia_list' need
seed_init.delete_dupefilter_key()
seed_init.delete_items_key()
seed_init.push_start_urls_key(start_url=start_url)

# 5. execute scrapy crawl woaiwojia_list
output_data = 'output/data/' + spider_name + '.json'
# output_log = '--logfile=output/logs/' + spider_name + '.log'
# execute(['scrapy', 'crawl', spider_name, '-o', output_data, output_log])
execute(['scrapy', 'crawl', spider_name, '-o', output_data])