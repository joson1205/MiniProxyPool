#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date        : 2019-07-04 14:41:43
# @Author      : Joson (joson1205@163.com)
# @Link        : github.com/joson1205
# @Description : 获取代理


import re
import time
from WebRequests import SetRequests


class GetFreeProxy(object):
    """docstring for GetFreeProxy"""

    # 快代理
    @staticmethod
    def kuaidaili(page_count=2):
        for page in range(1, page_count + 1):
            url = "https://www.kuaidaili.com/free/inha/{}/".format(page)
            web_requests = SetRequests()
            result = web_requests.getHTML(url)
            if result["code"]:
                proxies = re.findall(r'(?<=IP">).+?(?=<)|(?<=PORT">)\d+', result["data"])
                for i in range(0, len(proxies), 2):
                    yield "{}:{}".format(proxies[i], proxies[i + 1])
            time.sleep(1)

    # 免费代理IP库
    @staticmethod
    def jiangxianli(page_count=2):
        for i in range(1, page_count + 1):
            url = 'http://ip.jiangxianli.com/?page={}'.format(i)
            web_requests = SetRequests()
            result = web_requests.getHTML(url)
            if result["code"]:
                proxies = re.findall(r'(?<=data-ip=").+?(?=")|(?<=data-port=")\d+', result["data"])
                for i in range(0, len(proxies), 2):
                    yield "{}:{}".format(proxies[i], proxies[i + 1])


if __name__ == '__main__':
    freeProxy = GetFreeProxy()
    ip_list = freeProxy.jiangxianli()
    for ip in ip_list:
        print(ip)
