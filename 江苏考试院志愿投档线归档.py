import sqlite3
import xlrd	
import os


conn = sqlite3.connect("cee.db")
cur = conn.cursor()
#cur.execute("delete from collegeline where id>100000 and id< 200000 ")

score =	{ '文科'	: [] , '理科'	: [] }



def	load_order():
	f =	open('2021排名.csv','rt')
	for	l in f.readlines():
		fl = l.split(",")
		if fl[0] ==	'物理' :
			score['理科'].append(fl)
		else:
			score['文科'].append(fl)
	f.close()

#取得排名，同排名人数
def	get_order(n,type):
	od = 0 
	if type	== '理科':
		for	x in score['理科']:
			if int(x[1])<= n :
				return int(x[3])
			od += int(x[2])
	else:
		for	x in score['文科']:
			if int(x[1])<= n :
				return int(x[3])
			od += int(x[2])
	#return [od,1]
	return od
			

#[text:'院校\n代号', text:'院校、专业组\n（再选科目要求）', text:'定向地区', text:'投档\n最低分', text:'投档最低分同分考生排序项', empty:'',	empty:'', empty:'',	empty:'', empty:'',	empty:'']
#[empty:'',	empty:'', empty:'',	empty:'', text:'(一)',	text:'(二)', text:'(三)',	text:'(四)', text:'(五)',	text:'(六)', text:'(七)']
#[empty:'',	empty:'', empty:'',	empty:'', text:'高考文化分', text:'语数\n成绩', text:'语数\n最高\n成绩',	text:'外语\n成绩', text:'首选科目成绩', text:'再选科目最高成绩', text:'志\n愿\n号']
#[text:'1103', text:'南京航空航天大学09专业组(不限)', empty:'', number:209.0, number:355.0, number:128.0, number:86.0,	number:97.0, number:42.0, number:49.0, number:4.0]



load_order()

#print("575=%d" % (get_order(575,'理科')))
#os._exit(777)

rc=0
skip=0
id=100000
for	file in	os.listdir("data/jseea/"):
	if not file.endswith("xls"):
		continue
	#print(file)
	part = file.split('_')
	if int(part[0])	!= 2021	:
		continue
	#print("%s - %d"	% (file,id))
	name = "data/jseea/" + file	
	xls	= xlrd.open_workbook(name)
	table =	xls.sheets()[0]
	nr = table.nrows
	print("%s - %d - #%d"	% (file,id,nr))
	title =	''
	for	i in range(1,nr):
		row	= table.row(i)
		#print(row)
		ins = False
		if row[0].ctype	== 1 and len(row[0].value) > 2 and title ==	'' :
			title =	row[0].value
			title =	title.replace("\n","-")
			#print( title )
			f1 = "普" if title.find('普通类') != -1	else ('艺'	if title.find('艺术类') != -1 else "体"	)
			#title.find('艺术类')
			#title.find('体育类')
			f2 = "本" if title.find('本科') != -1 else "专"	
			#title.find('专科')
			f3 = "史" if title.find('历史等') != -1	else "物"
			if f3=='史' :
				tt = '文科'
			else:
				tt = '理科'
			#title.find('物理等')
			f4 = "前" if title.find('提前批次') !=	-1	else "常"
			f6 = "平2"	 if	title.find('第2小批平行志愿') !=	-1 else	('平' if title.find('平行志愿') !=	-1 else	"")
			if f6 == '':
				f6 = '征' if  title.find('征求志愿') != -1	else ''
			#title.find('平行志愿')
			f5 = "航" if title.find('—航海') != -1	else ""
			if f5 == '':
				f5 = "士" if title.find('—定向培养士官') != -1	else ""
			if f5 == '':
				f5 = "法" if title.find('—公安政法')	!= -1 else ""
			if f5 == '':
				f5 = "美" if title.find('—美术') != -1	else ""
			if f5 == '':
				f5 = "编" if title.find('—编导') != -1	else ""
			if f5 == '':
				f5 = "声" if title.find('—声乐') != -1	else ""
			if f5 == '':
				f5 = "器" if title.find('—器乐') != -1	else ""
			if f5 == '':
				f5 = "专" if title.find('—地方专项')	!= -1 else ""
			if f5 == '':
				f5 = "教" if title.find('—乡村教师计划') != -1	else ""
			if f5 == '':
				f5 = "其" if title.find('—其他院校')	!= -1 else ""
			flag = "%s-%s-%s-%s-%s-%s" % (f1,f2,f3,f4,f5,f6) 
			#print(flag)
			continue
		if row[0].ctype	== 1 and i > 3 :  # number	
			try:
				code = int(row[0].value)
			except:
				code = 0 
			if( code == 0 ):
				continue;
			#分数转位次
			try:
				sc = int(row[3].value)
			except:
				sc = int(row[0].value.splitlines()[0])
			wc = get_order(sc,tt)
			#	
			rl = len(row)
			print(" %d => %d len=%d " %  (sc ,wc , rl) )
			try:
				if( rl == 10 ):
					el = (id,flag,row[1].value,row[0].value,tt,'2021',flag,0,sc,sc,0,wc,row[3].value,wc,sc)
					sql	= "INSERT OR REPLACE INTO collegeline VALUES(%d,'%s','%s','%s','%s','%s','%s','%s',%d,%d,%d,'%s','%s',%d,%d);" % el	
					ins = True
				if( rl == 9 ):
					#分数转位次
					sc = int(row[2].value)
					wc = get_order(sc,tt)
					#
					el = (id,flag,row[1].value,row[0].value,tt,'2021',flag,0,sc,sc,0,wc,row[3].value,wc,sc)
					sql	= "INSERT OR REPLACE  INTO collegeline VALUES(%d,'%s','%s','%s','%s','%s','%s','%s',%d,%d,%d,'%s','%s',%d,%d);" % el	
					ins = True
				if( rl == 11 ):
					el = (id,flag,row[1].value,row[0].value,tt,'2021',flag,0,sc,sc,0,wc,row[3].value,wc,sc)
					sql	= "INSERT OR REPLACE  INTO collegeline VALUES(%d,'%s','%s','%s','%s','%s','%s','%s',%d,%d,%d,'%s','%s',%d,%d);" % el	
					ins = True
				if( rl == 13):
					el = (id,flag,row[1].value,row[0].value,tt,'2021',flag,0,sc,sc,0,wc,row[3].value,wc,sc)
					sql	= "INSERT OR REPLACE  INTO collegeline VALUES(%d,'%s','%s','%s','%s','%s','%s','%s',%d,%d,%d,'%s','%s',%d,%d);" % el	
					ins = True
			except:
				sql = ""
				skip = skip +1 				
				print("Error %d " % (rl))
			if( not ins ):
				print("file=%s,ctype=%d , len=%d , %s" % (file,row[0].ctype,len(row),row[0].value))
				for	i in range(0,len(row)):
					print("\t%s" % (str(row[i].value)))
			else:
				rc = rc + 1 
				id=id+1
				print(sql)
				cur.execute(sql)
				sql = ""
print(" total = %d \n" % (rc))


cur.execute("commit")


#ex	= xlrd.open_workbook("data/jseea/0b9566a7281d208ffbbbe15c9b975f48_0519087ee623bb83ae7f1db0c3f87f88.xls")
#table = ex.sheets()[0]
#nc	= table.ncols
#nr	= table.nrows 
#for i in range(1,nr):
#	 row = table.row(i)
#	 print(row)

'''
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