import os
import requests
from lxml import etree
import json
import hashlib

#apt install libjpeg62-dev libtiff-dev  
#apt install tesseract-ocr  tesseract-ocr-chi-sim



fil = "data/2021score/source.html"
src = "http://suzhou.bendibao.com/edu/2017717/64268.shtm"
headers = { 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' } 

if(os.path.exists(fil)):
    #如果存在直接读取内容
    print ( 'load from file %s' % (fil))
    f = open(fil,"rt")
    str = f.read()
    f.close()
else:
    #没有本地文件则从网络下载
    print ( 'load from network %s' % (src))
    response  = requests.get(src,headers = headers) 
    #结果保存到本地文件
    f = open(fil,"wt")
    f.write(response.text)
    f.close()
    str = response.text

tree = etree.HTML(str)
#定位到结果数据的行
i = tree.xpath("//div[@class='content']/p/img")
hasher = hashlib.md5()
filea = [] 
for x in i:
    link = x.xpath("./@src")[0]
    #print(link)
    hasher.update(link.encode('ascii'))
    md5str = hasher.hexdigest()
    fil = "data/2021score/%s.png" % (md5str)
    #print( "save %s to %s" % (link,fil))
    if not os.path.exists(fil):
        response  = requests.get(link,headers = headers) 
        f = open(fil,"wb")
        f.write( response.content )
        f.close()
    filea.append(fil)
print("load png success")

# ['eng' , 'osd' ]
#print(pytesseract.get_languages(config=''))

for x  in filea:
    dst = "%s.text" % (x)
    if os.path.exists(dst):
        continue
    cmd = "tesseract  %s %s -l eng+chi_sim"  % ( x , dst)
    print("OCR %s : %s " %(x,cmd))
    os.system(cmd)

