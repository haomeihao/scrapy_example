# -*- coding: utf-8 -*-
__author__ = 'hmh'

import requests
from scrapy.selector import Selector
from scrapy.utils.python import to_native_str
import redis
import time

redis_pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0)
redis_cli = redis.Redis(connection_pool=redis_pool)
key = 'xici_ip_proxy_pool'


# 爬去IP
def crawl_ips():
    # 爬取西刺的免费ip代理
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0"}

    for i in range(10):
        time.sleep(3)
        url = "http://www.xicidaili.com/nn/{0}".format(i + 1)
        print('请求地址: {0}'.format(url))
        proxy_dict = {
            "http": get_random_ip(),
        }
        re = None
        try:
            re = requests.get(url, headers=headers, proxies=proxy_dict)

            print('请求代理网站成功，开始解析页面')

            selector = Selector(text=re.text)
            all_trs = selector.css("#ip_list tr")

            ip_list = []
            for tr in all_trs[1:]:
                speed_str = tr.css(".bar::attr(title)").extract()[0]
                speed = 0
                if speed_str:
                    speed = float(speed_str.split("秒")[0])
                all_texts = tr.css("td::text").extract()

                ip = all_texts[0]
                port = all_texts[1]
                proxy_type = all_texts[5]

                ip_list.append((ip, port, proxy_type, speed))

            for ip_info in ip_list:
                ip = ip_info[0]
                port = ip_info[1]

                proxy_url = format_ip(ip, port)
                print('判断代理是否可用 proxy url: {0}, page: {1}'.format(proxy_url, str(i + 1)))
                flag = judge_ip(proxy_url)
                if flag:
                    redis_cli.sadd(key, proxy_url)

        except Exception as e:
            print("使用代理请求异常2 Exception: invalid ip and port")

# 格式化IP
def format_ip(ip, port):
    proxy_url = "http://{0}:{1}".format(ip, port)
    return proxy_url


# 判断IP是否可用
def judge_ip(proxy_url):
    # 判断ip是否可用
    http_url = "http://www.baidu.com"
    try:
        proxy_dict = {
            "http": proxy_url,
        }
        response = requests.get(http_url, proxies=proxy_dict)
    except Exception as e:
        print("使用代理请求异常 Exception: invalid ip and port")
        return False
    else:
        code = response.status_code
        if code >= 200 and code < 300:
            print("Effective ip and port {0}".format(proxy_url))
            return True
        else:
            print("Invalid ip and port {0}".format(proxy_url))
            return False


# 从redis中随机获取IP
def get_random_ip():
    # 从数据库中随机获取一个可用的ip
    proxy_url = redis_cli.srandmember(key)
    if proxy_url:
        proxy_url = to_native_str(proxy_url)
        judge_re = judge_ip(proxy_url)
        if judge_re:
            return proxy_url
    return get_random_ip()


# print (crawl_ips())
if __name__ == "__main__":
    # crawl_ips()
    print(get_random_ip())
