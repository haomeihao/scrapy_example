# coding = utf-8
"""
author: hmh
"""
import hashlib
import json
import re
import time
import datetime
import os
import logging
from typing import Iterable

from scrapy_example.project_path import get_project_path

logger = logging.getLogger(__name__)


# 控制台输出
def console(data, title, spider_name="baidu"):
    # print("##### " + title + " 开始...")
    # print(type(data))

    dict = {}
    for key, value in data.items():
        key = str(key).replace("b'", "").replace("'", "")
        value = str(value).replace("b'", "'").replace("'", "")
        dict[key] = value

    print_pretty(dict, title, spider_name)
    # print("##### " + title + " 结束...")


# 美化输出 json
def print_pretty(dict, title, spider_name):
    jsonstr = json.dumps(dict, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ':'))
    # print(jsonstr)

    timestr = str(get_time_stamp())
    write_to_file(jsonstr, timestr + "." + title, spider_name=spider_name)


# 从内存写入磁盘文件
def write_to_file(filedata, filename, datatype="headers", filetype="json", spider_name="baidu", mode='w'):
    parent_path = os.path.join(get_project_path(), "output" + os.sep + datatype + os.sep + spider_name)
    if not os.path.exists(parent_path):
        os.makedirs(parent_path)
    filename = os.path.join(parent_path, filename + "." + filetype)
    with open(filename, mode, encoding='utf-8') as file:
        file.write(filedata)
    # print("写入文件 " + filename + " 成功...")


# 将response.text写入html
def write_html_to_file(filedata, filename, spider_name):
    write_to_file(filedata, filename, "html", "html", spider_name)


# 清空目录下的所有文件
def delete_file(path):
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            delete_file(c_path)
        else:
            os.remove(c_path)
    # print("清空文件夹 " + path + " 成功...")


# 获取时间戳
def get_time_stamp():
    return int(round(time.time() * 1000))


# 格式化时间
def format_now_time():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


# 日志格式化时间
def log_now_time():
    return "[" + format_now_time() + "] "


# 格式化日期
def format_now_date(format="%Y-%m-%d"):
    return datetime.datetime.now().strftime(format)


# 获取日志文件路径+名称
def get_log_file(log_path="logs/scrapy"):
    project_path = get_project_path()
    parent_path = os.path.join(project_path, log_path)
    is_exists = os.path.exists(parent_path)
    if not is_exists:
        os.makedirs(parent_path)
    datestr = format_now_date(format='%Y%m%d')
    log_file = os.path.join(parent_path, datestr + '.log')
    return log_file


def get_millisecond_timestamp():
    return int(round(time.time() * 1000))


def get_second_timestamp():
    return int(round(time.time()))


def format_now_datetime(format_str='%Y-%m-%d %H:%M:%S'):
    return datetime.datetime.now().strftime(format_str)


# def format_now_date(format_str='%Y-%m-%d'):
#     return datetime.datetime.now().strftime(format_str)


# def format_now_time(format_str='%H:%M:%S'):
#     return datetime.datetime.now().strftime(format_str)


def get_project_dir():
    return os.path.dirname(os.path.dirname(__file__))


def format_json(dict):
    jsonstr = json.dumps(dict, ensure_ascii=False, indent=4)
    return jsonstr


def parse_to_dict(data):
    dict = {}
    if isinstance(data, Iterable):
        for key, value in data.items():
            key = str(key).replace("b'", "").replace("'", "")
            value = str(value).replace("b'", "'").replace("'", "")
            dict[key] = value
    return dict


def log_response(response):
    try:
        depth = str(response.meta.get('depth', 0))

        res_headers = parse_to_dict(response.headers)
        set_cookie = res_headers.get('Set-Cookie', 'None')
        x_via = res_headers.get('X-Via', 'None')

        dont_merge_cookies = str(response.request.meta.get('dont_merge_cookies', None))

        res_req_headers = parse_to_dict(response.request.headers)
        cookie = res_req_headers.get('Cookie', 'None')
        referer = res_req_headers.get('Referer', 'None')
        user_agent = res_req_headers.get('User-Agent', 'None')
        authorization = res_req_headers.get('Authorization', 'None')
        proxy_authorization = res_req_headers.get('Proxy-Authorization', 'None')

        return ('\n' + str(response.status) + ', ' + response.url + ', response.meta.depth: ' + depth
                + '\n, response.headers.Set-Cookie: ' + set_cookie
                + '\n, response.headers.X-Via: ' + x_via
                + '\n, response.request.meta.dont_merge_cookies: ' + dont_merge_cookies
                + '\n, response.request.headers.Cookie: ' + cookie
                + '\n, response.request.headers.Referer: ' + referer
                + '\n, response.request.headers.User-Agent: ' + user_agent
                + '\n, response.request.headers.Authorization: ' + authorization
                + '\n, response.request.headers.Proxy-Authorization: ' + proxy_authorization)
    except Exception as e:
        print(e)
        logger.error(e)


def log_simple_response(response):
    try:
        res_req_headers = parse_to_dict(response.request.headers)
        referer = res_req_headers.get('Referer', 'None')
        return str(response.status) + ', ' + response.url + ', response.meta.depth: ' + str(
            response.meta.get('depth', 0)) + ', response.request.headers.Referer: ' + referer
    except Exception as e:
        return str(
            response.status) + ', ' + response.url + ', response.meta.depth: None, response.request.headers.Referer: None'


def log_request(request):
    try:
        depth = str(request.meta.get('depth', 0))
        dont_merge_cookies = str(request.meta.get('dont_merge_cookies', None))

        send_cookies = request.cookies

        res_req_headers = parse_to_dict(request.headers)
        cookie = res_req_headers.get('Cookie', 'None')
        referer = res_req_headers.get('Referer', 'None')
        user_agent = res_req_headers.get('User-Agent', 'None')
        authorization = res_req_headers.get('Authorization', 'None')
        proxy_authorization = res_req_headers.get('Proxy-Authorization', 'None')

        return ('\n' + request.method + ', ' + request.url + ', request.meta.depth: ' + depth
                + '\n, request.meta.dont_merge_cookies: ' + dont_merge_cookies
                + '\n, request.cookies: ' + str(send_cookies)
                + '\n, request.headers.Cookie: ' + cookie
                + '\n, request.headers.Referer: ' + referer
                + '\n, request.headers.User-Agent: ' + user_agent
                + '\n, request.headers.Authorization: ' + authorization
                + '\n, request.headers.Proxy-Authorization: ' + proxy_authorization)
    except Exception as e:
        print(e)
        logger.error(e)


def log_simple_request(request):
    try:
        res_req_headers = parse_to_dict(request.headers)
        referer = res_req_headers.get('Referer', 'None')
        return request.method + ', ' + request.url + ', request.meta.depth: ' + str(
            request.meta.get('depth', 0)) + ', request.headers.Referer: ' + referer
    except Exception as e:
        return request.method + ', ' + request.url + ', request.meta.depth: None, request.headers.Referer: None'


def print_log_info(title='Hello Scrapy, ', content='I use Python'):
    print(log_now_time() + title + content)
    logging.info(title + content)


def print_log_error(title='Hello Scrapy, ', content='I use Python'):
    print(log_now_time() + title + content)
    logging.error(title + content)


def get_url_id(url):
    if not url:
        return None
    return url.split('/')[-1].split('.')[0]


def get_md5(url):
    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


def before_main_create_dir(spider_name="baidu"):
    project_path = get_project_path()
    output_path = os.path.join(project_path, "output")
    # filetypes = ['headers', 'html']
    filetypes = ['data', 'logs']
    # filetypes = ['headers', 'html', 'data', 'logs']
    for filetype in filetypes:
        parent_path = output_path + os.sep + filetype + os.sep + spider_name
        is_exists = os.path.exists(parent_path)
        if not is_exists:
            os.makedirs(parent_path)
            print(log_now_time() + "已创建 " + parent_path + " 目录, 可以开始啦...")


def before_main_remove_file(spider_name="baidu"):
    project_path = get_project_path()
    output_path = os.path.join(project_path, "output")
    # filetypes = ['headers', 'html']
    # filetypes = ['data', 'logs']
    filetypes = ['headers', 'html', 'data', 'logs']
    for filetype in filetypes:
        parent_path = output_path + os.sep + filetype + os.sep + spider_name
        is_exists = os.path.exists(parent_path)
        if is_exists:
            delete_file(parent_path)
            print(log_now_time() + "已清除 " + parent_path + " 目录下的旧文件, 准备开始吧...")
    time.sleep(1)

def pattern_url(body):
    pattern = r"('http.*');"
    url = re.search(pattern, body)
    if url:
        return url.group()[1:-2]
    else:
        return None

if __name__ == '__main__':
    url = "https://bj.5i5j.com/ershoufang/41984976.html"
    print((get_url_id(url)))
    print(get_md5(url))
