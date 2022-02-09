#!/usr/bin/python3.7



import os
import requests
from lxml import etree
import json

#该栏目共613页，所以生成范围1-613
for i in range(1,614):
    #生成网页连接
    url = "https://gaoxiao.jszs.com/CollegeLine/index/sname/0/s/0-0-0-0-%d.html#tips" % (i)   #1-613
    #生成本地存储文件
    fil = "data/hair/%d.html" % (i)    
    #检查本地是否存在
    if os.path.exists(fil) :
        #如果存在直接读取内容
        print ( 'load from file %s' % (fil))
        f = open(fil,"rt")
        str = f.read()
        f.close()
    else:
        #没有本地文件则从网络下载
        print ( 'load from network %s' % (fil))
        headers = { 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' } 
        response  = requests.get(url,headers = headers) 
        #结果保存到本地文件
        f = open(fil,"wt")
        f.write(response.text)
        f.close()
        str = response.text
    #生成中间数据文件名称
    fil = "data/hair/%d.json" % (i)
    #如果存在中间数据文件，则不重复处理
    if os.path.exists(fil):
        continue
    #结果数组
    rdict = []
    #print(str)
    #把网页提给分析器
    tree = etree.HTML(str)
    #定位到结果数据的行
    i = tree.xpath("//div[@class='msg_table']/table/tbody/tr")
    #print(len(i))
    for x in i:
        #当前行数据在x中，根据单元格的顺序分别取出不同的属性和数据
        school_link = x.xpath("./td[1]/a/@href")[0]
        school_name = x.xpath("./td[1]/a/text()")[0]
        code = x.xpath("./td[2]/text()")[0]
        cate = x.xpath("./td[3]/text()")[0]
        year = x.xpath("./td[4]/text()")[0]
        pici = x.xpath("./td[5]/text()")[0]
        jihua = x.xpath("./td[6]/text()")[0]
        zuigao = x.xpath("./td[7]/text()")[0]
        zuidi = x.xpath("./td[8]/text()")[0]
        fencha = x.xpath("./td[9]/text()")[0]
        diwei = x.xpath("./td[10]/text()")[0]
        diweishu = x.xpath("./td[11]/text()")[0]
        #把当前行的数据拼接到字典中去
        rec = { 'link' : school_link , 'name' : school_name , '招生代码' : code , '科类' : cate , '年份' : year , '批次':pici ,'录取数':jihua , '最高分':zuigao ,'最低分':zuidi,'分差':fencha,'最低分位次':diwei,'最低分位次考生数':diweishu}
        #把记录添加到结果数组
        rdict.append(rec)
    #把结果数组序列化成JSON格式，并保存起来
    f = open(fil,"wt")
    f.write( json.dumps(rdict,skipkeys=False,indent=' ',ensure_ascii=False))
    f.close()
    