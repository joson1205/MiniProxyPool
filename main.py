#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date        : 2019-07-08 17:06:59
# @Author      : Joson (joson1205@163.com)
# @Link        : github.com/joson1205
# @Description : 写入/更新数据库

import gevent
from gevent import monkey
monkey.patch_all()

import pymysql
from Config import mysql
from ValidProxy import CheckProxy
from ValidUsefulProxy import UsefulProxy


class DB(object):
    """docstring for DB"""

    def main(self):
        self.add_proxy()
        self.validRefresh()
        self.invalidDelete()

    def create_con(self):
        con = pymysql.connect(
            host=mysql["host"],
            port=mysql["port"],
            user=mysql["user"],
            password=mysql["password"],
            db=mysql["database"],
            charset=mysql["charset"],
            cursorclass=pymysql.cursors.DictCursor)
        cur = con.cursor()
        return con, cur

    def select_unknown_proxy(self):
        con, cur = self.create_con()
        print("开始验证代理!")
        # 导出需要验证的代理
        sql = """
            SELECT
                ip,ishttps,anonymous,last_succ_time,succ_count,fail_count,total,score,
                country,region,city,lat,lon,isp FROM proxy
            """
        cur.execute(sql)
        verify_proxy = cur.fetchall()
        cur.close()
        con.close()
        # 转字典格式
        verify_proxy_dict = dict()  # 待验证
        unknown_proxy = list()  # 待查询地址信息
        while verify_proxy:
            proxy = verify_proxy.pop()
            verify_proxy_dict[proxy["ip"]] = proxy
            if proxy["country"] == None:
                unknown_proxy.append(proxy["ip"])

        return verify_proxy_dict, unknown_proxy

    def add_proxy(self):
        con, cur = self.create_con()
        import warnings
        # 忽略插入数据重复PRIMARY警告
        warnings.filterwarnings("ignore")
        print("开始获取代理数据......")
        proxies = CheckProxy.getAllProxyFunc()
        data = list()
        for item in proxies.values():
            data.append((
                item["web"],
                item["ip"],
                item["ishttps"],
                item["anonymous"],
                item["succ_count"],
                item["fail_count"],
                item["total"],
                item["score"],
                item["last_succ_time"],
                item["create_time"]))
        sql = """
            INSERT IGNORE INTO proxy (
                web,ip,ishttps,anonymous,succ_count,fail_count,total,score,last_succ_time,create_time)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
        try:
            cur.executemany(sql, data)
            con.commit()
        except Exception as e:
            con.rollback()  # 事务回滚
            print('执行失败! 原因:', e)
        finally:
            cur.close()
            con.close()
        print("代理获取完毕!")

    def validRefresh(self):
        """验证代理,刷新数据库"""
        verify_proxy_dict, unknown_proxy = self.select_unknown_proxy()
        finished_proxy = UsefulProxy().main(verify_proxy_dict, unknown_proxy)
        print("开始刷新数据库信息...")
        insertData = list()
        for key in finished_proxy.keys():
            insertData.append((
                finished_proxy[key]["ip"],
                finished_proxy[key]["ishttps"],
                finished_proxy[key]["anonymous"],
                finished_proxy[key]["last_succ_time"],
                finished_proxy[key]["succ_count"],
                finished_proxy[key]["fail_count"],
                finished_proxy[key]["total"],
                finished_proxy[key]["score"],
                finished_proxy[key]["country"],
                finished_proxy[key]["region"],
                finished_proxy[key]["city"],
                finished_proxy[key]["lat"],
                finished_proxy[key]["lon"],
                finished_proxy[key]["isp"]
            ))

        sql = """
            INSERT INTO proxy (
                ip,ishttps,anonymous,last_succ_time,succ_count,fail_count,total,score,
                country,region,city,lat,lon,isp)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE
            ip=VALUES(ip),
            ishttps=VALUES(ishttps),
            anonymous=VALUES(anonymous),
            last_succ_time=VALUES(last_succ_time),
            succ_count=VALUES(succ_count),
            fail_count=VALUES(fail_count),
            total=VALUES(total),
            score=VALUES(score),
            country=VALUES(country),
            region=VALUES(region),
            city=VALUES(city),
            lat=VALUES(lat),
            lon=VALUES(lon),
            isp=VALUES(isp)
            """
        con, cur = self.create_con()
        try:
            cur.executemany(sql, insertData)
            con.commit()
        except Exception as e:
            con.rollback()  # 事务回滚
            print('执行失败! 原因:', e)
        finally:
            cur.close()
            con.close()
        print("完成!")

    def invalidDelete(self):
        """
        删除无效的代理
        总验证次数 > 100 AND 评分 < 0.3
        """
        sql = "DELETE FROM proxy WHERE total > 100 AND score < 0.3"
        con, cur = self.create_con()
        cur.execute(sql)
        con.commit()
        cur.close()
        con.close()


if __name__ == '__main__':
    DB().main()
