#!/usr/bin/python3.7

import sqlite3
import os
import sys
from texttable import Texttable

conn = sqlite3.connect("cee.db")
cur = conn.cursor()

table = Texttable()
table.set_cols_align(["c","c","c","c","c","c","c"])
table.add_row(['年份','学校名称','类别','批次','代码','位次','人数'])

#table.add_row(['年份','学校名称','类别','批次','代码','低分位次','低分批次人数'])

sql = "SELECT * FROM ( SELECT * FROM collegeline WHERE diweici_num < %d  and diweici_num>0 order by diweici_num desc limit 30 ) ORDER BY nianfen desc ,diweici_num desc " % (int(sys.argv[1])) 
cur.execute(sql)
for row in cur:
    #print(row)
    dat = [row[5],row[2],row[4],row[6],row[3],int(row[13]),int(row[14])]
    #print("|%7s|%20s|%4s|%12s|%6s|%6d|%6d|" % dat)
    table.add_row(dat)
table.add_row(['年份','学校名称','类别','批次','代码','位次','人数'])
print( table.draw() + "\n" )



'''
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