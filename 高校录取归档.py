#!/usr/bin/python3.7

import sqlite3
import json
import os


conn = sqlite3.connect("cee.db")
cur = conn.cursor()



id = 0 
for i in range(1,614):
    fil = "data/hair/%d.json" % (i)
    if os.path.exists(fil) :
        print ( 'load from file %s' % (fil))
        f = open(fil,"rt")
        str = f.read()
        f.close()
        recs  = json.loads(str);
    else:
        print("丢失:%s\n" % (fil) )
        continue
    for o in recs:
        id += 1
        #print( "%s %s\n" % (o['最低分位次'],o['最低分位次考生数'])) 
        i2 = int(o['最高分'])
        i3 = int(o['最低分'])
        i4 = int(o['分差'])
        if(len(o['最低分位次'])<2):
            ici = -2
        else:
            ici = int( o['最低分位次'][1:-2])
        if(len(o['最低分位次考生数'])<2):
            iren = -2 
        else:
            iren = int( o['最低分位次考生数'][1:-2])
        el = (id,o['link'],o['name'],o['招生代码'],o['科类'],o['年份'],o['批次'],o['录取数'],i2,i3,i4,o['最低分位次'],o['最低分位次考生数'],ici,iren)
        #print( "\t%s(%d) %s(%d)\n" % (o['最低分位次'],ici,o['最低分位次考生数'],iren))
        #break
        #print(el)
        #break
        sql = "INSERT INTO collegeline VALUES(%d,'%s','%s','%s','%s','%s','%s','%s',%d,%d,%d,'%s','%s',%d,%d)" % el 
        cur.execute(sql)
conn.commit()
conn.close()


'''
{ 
    'link' : school_link , 
    'name' : school_name , 
    '招生代码' : code , 
    '科类' : cate , 
    '年份' : year , 
    '批次':pici ,
    '录取数':jihua , 
    '最高分':zuigao ,
    '最低分':zuidi,
    '分差':fencha,
    '最低分位次':diwei,
    '最低分位次考生数':diweishu
}

sqlite3 cee.db
DROP TABLE collegeline;
CREATE TABLE collegeline(
    id int primary key , 
    lianjie varchar(128),
    xuexiao varchar(64),
    daima varchar(16),
    leibie varchar(8),
    nianfen varchar(16),
    pici varchar(16),
    jihua varchar(16),
    zuigao int ,
    zuidi  int , 
    fencha int ,
    diweici varchar(32),
    diweiren varchar(32),
    diweici_num int default -1 ,
    diweiren_num int  default -1 
);
'''