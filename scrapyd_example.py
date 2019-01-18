# coding=utf-8
"""
scrapyd example
"""
from scrapyd import config
from scrapyd import eggstorage, eggutils
from scrapyd import launcher, runner, scheduler
from scrapyd import webservice, website

import socket
import os

hostname = socket.gethostname()
print("hostname: " + hostname)

host = socket.gethostbyname(hostname)
print("host: " + host)

pid = os.getpid()
print("pid: " + str(pid))
