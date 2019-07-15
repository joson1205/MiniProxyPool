# MiniProxyPool
一个轻量级的IP代理池,基于Python3环境.部分文件源码参考了[jhao104](https://github.com/jhao104/proxy_pool)的项目,更改了存储方式.
有需要的朋友也可以自行搜索.   

![image](https://github.com/joson1205/MiniProxyPool/blob/master/example.jpg?raw=true)  

## 代码执行流程  
![image](https://github.com/joson1205/MiniProxyPool/blob/master/%E6%B5%81%E7%A8%8B%E5%9B%BE.png?raw=true)

## MySQL DDL
```MySQL
CREATE TABLE `proxy` (
  `web` varchar(30) DEFAULT NULL COMMENT '站点',
  `ip` varchar(21) NOT NULL COMMENT 'ip',
  `score` decimal(6,3) DEFAULT NULL COMMENT '可用率(成功次数/验证总次数)',
  `total` int(5) DEFAULT NULL COMMENT '总验证次数',
  `succ_count` int(5) DEFAULT NULL COMMENT '成功次数',
  `fail_count` int(5) DEFAULT NULL COMMENT '失败次数',
  `last_succ_time` datetime DEFAULT NULL COMMENT '最后一次检查成功时间',
  `create_time` datetime DEFAULT NULL COMMENT '入库时间',
  `ishttps` int(1) DEFAULT NULL COMMENT '1/https_0/http',
  `anonymous` int(1) DEFAULT NULL COMMENT '1/匿名_0/透明',
  `country` varchar(20) DEFAULT NULL COMMENT '国家',
  `region` varchar(20) DEFAULT NULL COMMENT '地区',
  `city` varchar(20) DEFAULT NULL COMMENT '城市',
  `lat` varchar(10) DEFAULT NULL COMMENT '纬度',
  `lon` varchar(10) DEFAULT NULL COMMENT '经度',
  `isp` varchar(10) DEFAULT NULL COMMENT '运营商',
  PRIMARY KEY (`ip`),
  KEY `ip` (`ip`) USING BTREE,
  KEY `country` (`country`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```
## 配置
```Python
# MySQL
mysql = {
    "host": "host",
    "user": "root",
    "password": "password",
    "port": 3306,
    "database": "my_db",
    "charset": "utf8"
}
```
## 新增代理
```Python
# 修改 getFreeProxy.py
class GetFreeProxy(object):
    # ....
    # 你自己的方法
    @staticmethod
    def freeProxyCustom():  # 定义自己的代理名称
        # 通过某网站或者某接口或某数据库获取代理 任意你喜欢的姿势都行
        # 假设你拿到了一个代理列表
        proxies = ["139.129.166.68:3128", "139.129.166.61:3128", ...]
        for proxy in proxies:
            yield proxy
        # 确保每个proxy都是 host:ip正确的格式就行
```
## 使用
* 安装依赖库
```Python
pip install requests gevent pymysql
```
* 执行
```Python
Python main.py
```
