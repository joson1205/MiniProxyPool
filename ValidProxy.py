#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date        : 2019-07-09 12:28:25
# @Author      : Joson (joson1205@163.com)
# @Link        : github.com/joson1205
# @Description : 检查代理抓取情况

import re
import time
from getFreeProxy import GetFreeProxy


class CheckProxy(object):
    """docstring for CheckProxy"""
    @staticmethod
    def ValidProxyFormat(proxy):
        """验证代理格式"""
        verify_regex = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}"
        _proxy = re.findall(verify_regex, proxy)
        return True if len(_proxy) == 1 and _proxy[0] == proxy else False

    @staticmethod
    def getAllProxyFunc():
        """获取所有代理函数"""
        import inspect
        member_list = inspect.getmembers(GetFreeProxy, predicate=inspect.isfunction)
        proxy_dict = dict()
        for func_name, func in member_list:
            for ip in func():
                if CheckProxy.ValidProxyFormat(ip):
                    # 预设值
                    proxy_dict[ip] = {
                        "web": func_name,
                        "ip": ip,
                        "ishttps": 0,
                        "anonymous": 0,
                        "succ_count": 0,
                        "fail_count": 0,
                        "total": 0,
                        "score": 0,
                        "create_time": time.strftime("%Y-%m-%d %X", time.localtime()),
                        "last_succ_time": time.strftime("%Y-%m-%d %X", time.localtime())}
        return proxy_dict


if __name__ == '__main__':
    pp = CheckProxy.getAllProxyFunc()
    for p in pp:
        print(pp)
