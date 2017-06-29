#!/usr/bin/python

import time
import datetime
import sqlite3
import csv

def publish_future(cursor, row):
#{
	#create table
	try: 
		cursor.execute('''CREATE TABLE IF NOT EXISTS %s 
				(epoch INT PRIMARY KEY  NOT NULL,
				 ltp REAL NOT NULL
				);''' %(row[0]))
	except:	
		print "Could not create table %s" %(row[0])
		pass
	
	try:
		cursor.execute('''INSERT INTO %s
			VALUES (%d, %f)''' %(row[0], row[1], row[2]))	
	except:	
		print "Could not insert into table %s" %(row[1])
		pass
	print "inserted : %s" %(row)
#}


conn = sqlite3.connect('marcopolo.db')
print "Opened database successfully";

cursor=conn.cursor()
print "Got cursor for the connection";

hist_data=[]

with open('hist_data/all_data.csv', 'rb') as f:
	reader = csv.reader(f)
	hist_data = list(reader)

for row in hist_data:
#{
	index = row[0]

	expiry_date=datetime.datetime.strptime(row[2], '%d-%b-%Y')
	expiry=expiry_date.strftime('%d%b%Y').upper()

	todays_date=datetime.datetime.strptime(row[1], '%d-%b-%Y')
	epoch=int(todays_date.strftime('%s'))
	
	symbol = index + '_' + expiry
	openEpoch = epoch + 33300 
	highEpoch = epoch + 43200
	lowEpoch = epoch + 50400 
	closeEpoch = epoch + 55800 
	ltpEpoch = epoch + 56000 

	op = float(row[3].replace(',',''))
	hp = float(row[4].replace(',',''))
	lp = float(row[5].replace(',',''))
	cp = float(row[6].replace(',',''))
	ltp = float(row[7].replace(',',''))

	publish_future(cursor, [symbol, openEpoch, op])
	publish_future(cursor, [symbol, highEpoch, hp])
	publish_future(cursor, [symbol, lowEpoch, lp])
	publish_future(cursor, [symbol, closeEpoch, cp])
	publish_future(cursor, [symbol, ltpEpoch, ltp])

	#publish_row_to_db(cursor, row)
#}
conn.commit()
conn.close()
