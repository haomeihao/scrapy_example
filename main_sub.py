# coding=utf-8

import sys
import os
from scrapy.cmdline import execute

from redis_counter_init import RedisCounterInit
from scrapy_example.utils import before_main_create_dir, before_main_remove_file


# 注意这行代码必须加上 否则配置的输出文件路径有问题
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# only modify this spider_name is ok
# spider_name = 'woaiwojia_detail'
spider_name = 'oschina_company_detail'

# 1. before main create directory folder
before_main_create_dir(spider_name=spider_name)

# 2. init a counter
counter_init = RedisCounterInit(spider_name=spider_name)
counter_init.init()

# 3. execute scrapy crawl woaiwojia_detail
output_data = 'output/data/' + spider_name + '.json'
output_log = '--logfile=output/logs/' + spider_name + '.log'
execute(['scrapy', 'crawl', spider_name, '-o', output_data, output_log])
