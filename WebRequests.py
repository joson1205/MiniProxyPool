#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date        : 2019-07-08 17:41:50
# @Author      : Joson (joson1205@163.com)
# @Link        : github.com/joson1205
# @Description : 设置请求

import requests
import random
import time


class SetRequests(object):
  def user_agent(self):
    ua_list = [
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)"]
    return random.choice(ua_list)

  def headers(self):
    headers = {'User-Agent': self.user_agent(),
               'Accept': '*/*',
               'Connection': 'keep-alive',
               'Accept-Language': 'zh-CN,zh;q=0.8'}
    return headers

  def getHTML(self, url, retry_time=5, timeout=10, retry_interval=1):
    """
    retry_time:重试次数
    timeout:超时时间
    retry_interval:重试间隔时间
    """
    while True:
      try:
        headers = self.headers()
        res = requests.get(url, headers=headers, timeout=timeout)
        if res.status_code == 200:
            return {"code": True, "data": res.text}
        else:
          raise Exception
      except Exception as e:
        retry_time -= 1
        if retry_time <= 0:
          # 多次请求失败
          return {"code": False, "message": e}
        time.sleep(retry_interval)


if __name__ == '__main__':
  webRequests = SetRequests()
  tager_url = "http://ip-api.com/json/?lang=zh-CN"
  result = webRequests.getResponse(url=tager_url, html_type="JSON")
  print(result)
