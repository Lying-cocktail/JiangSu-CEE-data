import os
import requests
from lxml import etree
import hashlib
import re 

md5 = hashlib.md5()



base = "https://www.jseea.cn/search/?field=title&orderField=publishDate&wd=%E5%BF%97%E6%84%BF%E6%8A%95%E6%A1%A3%E7%BA%BF&pageIndex="
headers = { 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' } 

for i in range(1,17):
    url = base + "%d" % (i)
    fil = "data/jseea/%d.htm"  % (i)
    if os.path.exists(fil) :
        #如果存在直接读取内容
        print ( 'load from file %s' % (fil))
        f = open(fil,"rt")
        str = f.read()
        f.close()
    else:
        #没有本地文件则从网络下载
        print ( 'load from network %s' % (url))
        response  = requests.get(url,headers = headers) 
        #结果保存到本地文件
        f = open(fil,"wt")
        f.write(response.text)
        f.close()
        str = response.text
    tree = etree.HTML(str)
    ar = tree.xpath("//div[@class='search-result-item']/h3/a[2]")
    for x in ar:
        link = x.xpath("./@href")[0]
        text = x.xpath("./text()")
        slink = "https:" + link 
        print("found link:" + slink)
        print("     text: %s " % (text))
        md5.update(slink.encode('ascii'))
        smd5 = md5.hexdigest()
        fil = "data/jseea/%s.html" %(smd5)
        if os.path.exists(fil):
            print("    load %s" %(fil))
            f = open(fil,"rt")
            str = f.read()
            f.close()
        else:
            response  = requests.get(slink,headers = headers) 
            f = open(fil,"wt")
            f.write(response.text)
            f.close()
            str = response.text
        pattern = r'www.jseea.cn(.+?)xls'
        rslt = re.findall(pattern,str)
        for xls in rslt:
            url = "https://www.jseea.cn" + xls + "xls";
            part = xls.split('/')
            #print(part)
            md5.update(url.encode('ascii'))
            xlsmd5 = md5.hexdigest()
            if part[3] == 'old':
                fil = "data/jseea/%s_%s_%s.xls" % (part[6],smd5,xlsmd5)
            else:
                fil = "data/jseea/%s_%s_%s.xls" % (part[3],smd5,xlsmd5)
            print( "loading  %s" % (url))
            if not os.path.exists(fil):
                response = requests.get(url,headers=headers)
                f = open(fil,"wb")
                f.write( response.content )
                f.close()
        

 


