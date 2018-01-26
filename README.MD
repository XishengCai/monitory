# Monitor
<img src="https://travis-ci.org/guohongze/adminset.svg?branch=master"></img> 
<img src="https://img.shields.io/hexpm/l/plug.svg"></img>
[![release](https://img.shields.io/github/release/guohongze/adminset.svg)](https://github.com/guohongze/adminset/releases)
<br>
Monitor 是基于psutil开发的分布式监控服务器性能告警的脚本，一旦发生资源过载，即可通过邮件通知。

## 开发环境
centos7.2  python2.7 psutil5.4.3<br>

## 服务端
修改 Emial 初始化代码
防火墙对端口 40002 UPD放行
python server.py

## 客户端
修改 服务端ip地址
运行 python agent.py
