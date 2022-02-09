#!/usr/bin/python3.7



import os
import requests
from lxml import etree
import json


for i in range(1,614):
    url = "https://gaoxiao.jszs.com/CollegeLine/index/sname/0/s/0-0-0-0-%d.html#tips" % (i)   #1-613
    fil = "data/hair/%d.html" % (i)
    if os.path.exists(fil) :
        print ( 'load from file %s' % (fil))
        f = open(fil,"rt")
        str = f.read()
        f.close()
    else:
        print ( 'load from network %s' % (fil))
        headers = { 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' } 
        response  = requests.get(url,headers = headers) 
        f = open(fil,"wt")
        f.write(response.text)
        f.close()
        str = response.text
    fil = "data/hair/%d.json" % (i)
    #if os.path.exists(fil):
    #    continue
    rdict = []
    #print(str)
    tree = etree.HTML(str)
    i = tree.xpath("//div[@class='msg_table']/table/tbody/tr")
    #print(len(i))
    for x in i:
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
        rec = { 'link' : school_link , 'name' : school_name , '招生代码' : code , '科类' : cate , '年份' : year , '批次':pici ,'录取数':jihua , '最高分':zuigao ,'最低分':zuidi,'分差':fencha,'最低分位次':diwei,'最低分位次考生数':diweishu}
        rdict.append(rec)
    f = open(fil,"wt")
    f.write( json.dumps(rdict,skipkeys=False,indent=' ',ensure_ascii=False))
    f.close()
    