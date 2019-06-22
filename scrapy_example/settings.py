# -*- coding: utf-8 -*-

# Scrapy settings for scrapy_example project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import os
import threading
from scrapy_example.utils import log_now_time

BOT_NAME = 'scrapy_example'

SPIDER_MODULES = ['scrapy_example.spiders']
NEWSPIDER_MODULE = 'scrapy_example.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'scrapy_example (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = True
# 启用 cookies debug 模式 控制台会输出 set-cookie
COOKIES_DEBUG = True
# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    # 'Accept-Encoding': 'gzip, deflate, br',
    # 'Accept-Language': 'zh-CN,zh;q=0.9',
    # 'Cache-Control': 'max-age=0',
    # 'Connection': 'keep-alive',
    # 'Upgrade-Insecure-Requests': 1,
    # 'User-Agent': '"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",'

    ":authority": "www.mfcclub.com",
    ":scheme": "https",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9",
    "alexatoolbar-alx_ns_ph": "AlexaToolbar/alx-4.0.3",
    "cache-control": "max-age=0",
    "upgrade-insecure-requests": 1
}
PROXY_LIST = [
    # 'http://账号:密码@IP:PORT',
]
USER_AGENT_LIST = [
    "Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.60 Safari/537.17",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.15 (KHTML, like Gecko) Chrome/24.0.1295.0 Safari/537.15",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.14 (KHTML, like Gecko) Chrome/24.0.1292.0 Safari/537.14",
    "Opera/9.80 (Windows NT 6.1; U; ko) Presto/2.7.62 Version/11.00",
    "Opera/9.80 (Windows NT 6.1; U; fi) Presto/2.7.62 Version/11.00",
    "Opera/9.80 (Windows NT 6.1; U; en-GB) Presto/2.7.62 Version/11.00",
    "Opera/9.80 (Windows NT 6.1 x64; U; en) Presto/2.7.62 Version/11.00",
    "Opera/9.80 (Windows NT 6.0; U; en) Presto/2.7.39 Version/11.00",
    "Mozilla/5.0 (Windows NT 6.2; Win64; x64;) Gecko/20100101 Firefox/20.0",
    "Mozilla/5.0 (Windows x86; rv:19.0) Gecko/20100101 Firefox/19.0",
    "Mozilla/5.0 (Windows NT 6.1; rv:6.0) Gecko/20100101 Firefox/19.0",
    "Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/18.0.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:17.0) Gecko/20100101 Firefox/17.0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; nb-NO) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; fr-FR) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-TW) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; ru-RU) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; zh-cn) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5"
]
RANDOM_UA_TYPE = "random"
# DYNAMIC_REQUEST_HEADERS_HOST = [
#     'www.baidu.com'
# ]
# DYNAMIC_REQUEST_HEADERS_REFERER = [
#     'https://www.baidu.com/'
# ]

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# {
#     'scrapy.spidermiddlewares.httperror.HttpErrorMiddleware': 50,
#     'scrapy.spidermiddlewares.offsite.OffsiteMiddleware': 500,
#     'scrapy.spidermiddlewares.referer.RefererMiddleware': 700,
#     'scrapy.spidermiddlewares.urllength.UrlLengthMiddleware': 800,
#     'scrapy.spidermiddlewares.depth.DepthMiddleware': 900,
# }
#  Low orders are closer to the engine, high orders are closer to the spider.
SPIDER_MIDDLEWARES = {
    # 'scrapy_example.middlewares.ScrapyExampleSpiderMiddleware': 200,
    'scrapy_example.middlewares.CustomHttpErrorSpiderMiddleware': 45,
    'scrapy.spidermiddlewares.httperror.HttpErrorMiddleware': 50,
    # scrapy_splash
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}

HTTPERROR_ALLOWED_CODES = [302, 403, 503]

HTTPERROR_RETRY_ENABLED = True
HTTPERROR_RETRY_TIMES = 2
HTTPERROR_RETRY_CODES = [403, 302, 200]
HTTPERROR_RETRY_PRIORITY_ADJUST = 1

# {
#     'scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware': 100,
#     'scrapy.downloadermiddlewares.httpauth.HttpAuthMiddleware': 300,
#     'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware': 350,
#     'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware': 400,
#     'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': 500,
#     'scrapy.downloadermiddlewares.retry.RetryMiddleware': 550,
#     'scrapy.downloadermiddlewares.ajaxcrawl.AjaxCrawlMiddleware': 560,
#     'scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware': 580,
#     'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 590,
#     'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': 600,
#     'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': 700,
#     'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 750,
#     'scrapy.downloadermiddlewares.stats.DownloaderStats': 850,
#     'scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware': 900,
# }
# Low orders are closer to the engine, high orders are closer to the downloader.
DOWNLOADER_MIDDLEWARES = {
    # 'scrapy_example.middlewares.ScrapyExampleDownloaderMiddleware': 300,
    # 以下这个默认的代理不能禁用，否则会抛异常
    # Could not open CONNECT tunnel with proxy 10.28.80.246:8080 [{'status': 407, 'reason': b'Proxy Authorization Required'}]
    # 'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 750,
    'scrapy_example.middlewares.ProxyDownloaderMiddleware': 760,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_example.middlewares.UserAgentDownloaderMiddleware': 510,
    # 注意以下两个的顺序 响应必须先经过自定义的 downloader 值越大 响应先经过
    # 'crapy.downloadermiddlewares.retry.RetryMiddleware': 550,
    'scrapy_example.middlewares.RetryDownloaderMiddleware': 560,
    # 'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': 700,
    'scrapy_example.middlewares.CookieJarDownloaderMiddleware': 710,
    'scrapy_example.middlewares.CookieDownloaderMiddleware': 720,
    # scrapy_splash
    # 'scrapy_splash.SplashCookiesMiddleware': 723,
    # 'scrapy_splash.SplashMiddleware': 725,
}
# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'scrapy_example.pipelines.ScrapyExamplePipeline': 400,
    'scrapy_example.pipelines.CustomRedisPipeline': 410,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = False
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = True

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# 不要默认，设置1 默认是0.5-1.5
# 'AUTOTHROTTLE_ENABLED': True,
DOWNLOAD_DELAY = 5
# 不要默认，设置小点 默认是32
CONCURRENT_REQUESTS = 1

# 请求最大深度 默认0 不限制
# class scrapy.spidermiddlewares.depth.DepthMiddleware
DEPTH_LIMIT = 3
# verbose_stats 冗长统计
DEPTH_STATS = True
DEPTH_STATS_VERBOSE = True
# 深度优先策略 默认0不处理 正值先进行广度爬行 负值先进行深度爬行
DEPTH_PRIORITY = 1
SCHEDULER_DISK_QUEUE = 'scrapy.squeues.PickleFifoDiskQueue'
SCHEDULER_MEMORY_QUEUE = 'scrapy.squeues.FifoMemoryQueue'

# url 去重 开启 debug 模式
# DUPEFILTER_CLASS = 'scrapy.dupefilters.RFPDupeFilter'
# DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# DUPEFILTER_CLASS = "scrapy_redis_bloomfilter.dupefilter.RFPDupeFilter"
DUPEFILTER_CLASS = "scrapy_example.redis_dupefilters.CustomRedisSetDupeFilter"
# DUPEFILTER_CLASS = "scrapy_example.dupefilters.BloomFilterDupeFilter"
DUPEFILTER_DEBUG = True
# redis 去重依赖调度器 一并配置 要和去重过滤器配置一致
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# SCHEDULER = "scrapy_redis_bloomfilter.scheduler.Scheduler"
SCHEDULER_PERSIST = True

# Bloomfilter must be configure these two items
# Number of Hash Functions to use, defaults to 6
BLOOMFILTER_HASH_NUMBER = 6
# Redis Memory Bit of Bloomfilter Usage, 30 means 2^30 = 128MB, defaults to 30
BLOOMFILTER_BIT = 10

# Redis URL
# local
REDIS_URL = 'redis://127.0.0.1:6379'
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379

REDIS_START_URLS_AS_SET = False

# 日志级别
# LOG_LEVEL = 'WARN'
# LOG_LEVEL = 'INFO'
LOG_LEVEL = 'DEBUG'
# 日志格式 默认 '%(asctime)s [%(name)s] %(levelname)s: %(message)s'
# 2018-11-27 09:30:17 [scrapy.core.engine] INFO: Spider opened
LOG_FORMAT = '%(asctime)s [%(process)d-%(processName)s %(thread)d-%(threadName)s] [%(name)s] %(levelname)s: %(message)s'

# 是否把 standard 输出到 log 文件
# LOG_STDOUT = True

# 日志输出
# from scrapy_example.utils import get_log_file

# LOG_FILE = get_log_file()

# The encoding to be used for the feed
# Use utf-8 if you want UTF-8 for JSON too.
# 效果相当于 json.dumps(ensure_ascii=False)
FEED_EXPORT_ENCODING = 'utf-8'

# 将 sources 路径加进来
import sys

base_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(base_dir, 'scrapy_example'))

pinfo = (str(os.getpid()) + '-' + str(os.getppid()) + '-' + threading.current_thread().getName())
print(log_now_time() + pinfo)
