# JiangSu-CEE-data
# 江苏高考分析助手
---
数据来源：gaoxiao.jszs.com
---
运行环境：python3.7 + lxml  + Texttable 
---
原理：
* 高校录取数据.py - 爬虫，自动抓取历年录取信息保存并生成相应的json文件
* 高校录取归档.py - 把爬虫生成的json数据保存到sqlite数据
* 查询.py - 参数是全省位次，找出历年该位次区间的学生被哪些学校所收档，为自己填报志愿提供一点参考