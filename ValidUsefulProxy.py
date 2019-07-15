#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date        : 2019-07-11 17:13:44
# @Author      : Joson (joson1205@163.com)
# @Link        : github.com/joson1205
# @Description : Valid Useful Proxy

import gevent
from gevent import monkey
monkey.patch_all()

import time
import requests
from WebRequests import SetRequests


class UsefulProxy(object):
    """docstring for UsefulProxy"""

    def __init__(self):
        self.headers = SetRequests().headers()
        self.req = requests.session()

    def score(self, proxy, status_code, data=None):
        """
        status_code:布尔值
        data:查询后返回的数据
        对代理检测结果评分
        """
        if status_code:
            self.verify_proxy_dict[proxy]["ishttps"] = 1 if data["headers"]["X-Forwarded-Proto"] == "https" else 0
            self.verify_proxy_dict[proxy]["anonymous"] = 1 if data["headers"]["X-Real-Ip"] == proxy.split(":")[0] else 0
            self.verify_proxy_dict[proxy]["last_succ_time"] = time.strftime("%Y-%m-%d %X", time.localtime())
            self.verify_proxy_dict[proxy]["succ_count"] = self.verify_proxy_dict[proxy]["succ_count"] + 1
        else:
            self.verify_proxy_dict[proxy]["fail_count"] = self.verify_proxy_dict[proxy]["fail_count"] + 1

        self.verify_proxy_dict[proxy]["total"] = self.verify_proxy_dict[proxy]["total"] + 1
        self.verify_proxy_dict[proxy]["score"] = round(
            self.verify_proxy_dict[proxy]["succ_count"] / self.verify_proxy_dict[proxy]["total"], 3)

    def validUsefulProxy(self, proxy):
        """验证代理可用性"""
        # url = "http://ip-api.com/json/?lang=zh-CN"
        # url = "http://httpbin.org/ip"
        url = "http://httpbin.org/get?show_env=1"
        proxies = {
            "http": "http://{}".format(proxy),
            "https": "http://{}".format(proxy),
        }
        data = None
        try:
            res = self.req.get(url, headers=self.headers, proxies=proxies, timeout=10, verify=False)
            if res.status_code == 200 and res.json().get("headers"):
                status_code = True
                data = res.json()
            else:
                raise Exception
        except Exception as e:
            status_code = False
        self.score(proxy, status_code, data)

    def thread_run(self):

        threads_1 = [gevent.spawn(self.validUsefulProxy, key) for key in self.verify_proxy_dict.keys()]
        gevent.joinall(threads_1)
        print("代理验证完毕!")
        threads_2 = [gevent.spawn(self.validAddress, proxy) for proxy in self.unknown_proxy]
        gevent.joinall(threads_2)
        print("代理地址信息查询完毕!")

    def validAddress(self, proxy):
        """
        验证代理地址信息
        """
        url = "http://ip.taobao.com/service/getIpInfo.php?ip=" + proxy.split(":")[0]
        try:
            res = self.req.get(url, headers=self.headers, timeout=5, verify=False)
            if res.status_code == 200 and res.json()["code"] == 0:
                result = res.json()
                self.verify_proxy_dict[proxy]["country"] = result["data"]["country"]
                self.verify_proxy_dict[proxy]["region"] = result["data"]["region"]
                self.verify_proxy_dict[proxy]["city"] = result["data"]["city"]
                # self.verify_proxy_dict[proxy]["lat"] = result["data"]["lat"]
                # self.verify_proxy_dict[proxy]["lon"] = result["data"]["lon"]
                self.verify_proxy_dict[proxy]["isp"] = result["data"]["isp"]
        except Exception as e:
            pass

    def main(self, verify_proxy_dict, unknown_proxy):
        """
        verify_proxy_dict:已入库的代理
        unknown_proxy:信息不齐全代理
        """
        self.verify_proxy_dict = verify_proxy_dict
        self.unknown_proxy = unknown_proxy
        self.thread_run()
        return self.verify_proxy_dict


if __name__ == '__main__':
    kk = [{'ip': '1.192.240.5:9999', 'anonymous': 0, 'last_succ_time': "2019-07-12 16:43:31", 'succ_count': 0, 'fail_count': 0, 'total': 0, 'score': 0}, {
        'ip': '1.192.241.79:9999', 'anonymous': 0, 'last_succ_time': "2019-07-12 16:43:31", 'succ_count': 0, 'fail_count': 0, 'total': 0, 'score': 0}]

    print(tt)
