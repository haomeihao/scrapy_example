[TOC]
## Python爬虫框架Scrapy
``` 
Hello Scrapy, I use Python.
```
![背景](file/background.jpg)

### 一、项目依赖
#### 1.1 单机爬虫依赖
```
1) python 3.5+ 运行环境支持 [强烈建议使用 python 3.5+]
安装 python 3.5+ 运行时环境
2) 基于 python 的业界知名爬虫框架 scrapy
> pip install scrapy
```

#### 1.2 分布式爬虫依赖
```
1) redis K-V中间件
安装 redis-server 下载压缩包，解压即可用
2) python 的 redis 客户端库 redis-py [官网唯一打星的]
> pip install redis
3) scrapy 的 redis 分布式支持
> pip install scrapy-redis
4) 基于 scrapy-redis 的布隆过滤器支持 [bloomfilter 嵌入 scrapy-redis]
> pip install scrpay-redis-bloomfilter
```
#### 1.3 爬虫项目发布依赖

``` 
1) scrapyd webservice [官方推荐的发布工具 scrapyd]
> pip install scrapyd
2) scrapyd-client command [通过命令把项目打包推送到 scrapyd ]
> pip install scrapyd-client
3) scrapyd webui management [简单易用的 scrapyd webui 管理后台]
> pip install scrapydweb
```

### 二、项目运行初始化
``` 
1) 看下上面的项目依赖 进行必要的安装
或者 在根目录下执行下面的命令 一键安装 python lib 依赖
> pip install -r requirements.txt
注意: 分布式爬虫要安装 redis-server

2) 启动 redis-server
> redis-server.exe redis.windows.conf

启动 redis-cli [废弃]
> redis-cli.exe -h 127.0.0.1 -p 6379
在 redis-cli 交互式窗口 执行以下指令向 redis 推送一条初始化数据 [废弃]
> RPUSH woaiwojia_list:start_urls https://bj.5i5j.com/ershoufang/
以上两步已在 main.py 中做了初始化

3) 配置好 main.py 执行 main.py 进行启动即可
main.py 主spider 生产者 开启一个进程即可
main_sub.py 从spider 消费者 可开启多个进程
```

### 三、注意事项

#### 3.1 项目配置文件
``` 
项目相关的配置在 scrapy_example/settings.py 
redis key 相关的配置在 scrapy_example/redis_defaults.py 
```

#### 3.2 代理正确配置(可忽略)
```
 在项目目录下的 scrapy_example/settings.py 文件 修改
 PROXY_LIST = [
    'http://账号:密码@IP:PORT',
]
标准格式: http://username:password@some_proxy_server:port

注意: 当 'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': None 时，
不加账号和密码也可以，但是偶尔会提示输入账号密码，建议加上。
```

#### 3.3 安装异常(可忽略)
``` 
error: Microsoft Visual C++ 14.0 is required. Get it with "Microsoft Visual C+
+ Build Tools": https://visualstudio.microsoft.com/downloads/
解决方案: https://blog.csdn.net/weixin_42057852/article/details/80857948

error: command 'c:\\program files (x86)\\microsoft visual studio 14.0\\vc\\b in\\x86_amd64\\cl.exe' 
failed with exit status 2
解决方案: 离线下载 Twisted-18.9.0 进入目录 python setup.py install -> ok

删除 requirements.txt 中的 Twisted==18.7.0
再执行 pip install -r requirements.txt

还是不行 解决方案见 https://blog.csdn.net/jiangyunsheng147/article/details/80449556
去这个网站 https://www.lfd.uci.edu/~gohlke/pythonlibs/#twisted
下载对应版本的whl文件 Twisted‑18.9.0‑cp37‑cp37m‑win_amd64.whl
进入目录执行 pip install Twisted‑18.9.0‑cp37‑cp37m‑win_amd64.whl

各种问题: 
  File "O:\setup\Anaconda3\lib\site-packages\cryptography\hazmat\bindings\openssl\binding.py", line 172, in <module>
    Binding.init_static_locks()
  File "O:\setup\Anaconda3\lib\site-packages\cryptography\hazmat\bindings\openssl\binding.py", line 142, in init_static_locks
    __import__("_ssl")
ImportError: DLL load failed: 找不到指定的模块
解决思路: https://blog.csdn.net/blueheart20/article/details/79612985
总结: Python在跨平台、版本控制方面弱爆了，问题太多。

pip is configured with locations that require TLS/SSL, however the ssl module in Python is not available.

Caused by SSLError("Can't connect to HTTPS URL because the SSL module is not available.")

把 Anaconda3 换成之前 系统安装的Python3.5之后 就没问题了

```

## Python数据分析
### 一、Pandas
