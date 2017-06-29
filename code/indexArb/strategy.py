#!/usr/bin/python

import time
import datetime
import sqlite3
import csv

conn = sqlite3.connect('marcopolo.db')
print "Opened database successfully";

cursor=conn.cursor()
print "Got cursor for the connection";

index='NIFTY'
expiries = ['25AUG2016', '29SEP2016', '27OCT2016', '24NOV2016', '29DEC2016', '25JAN2017', '23FEB2017', '30MAR2017', '27APR2017', '25MAY2017', '29JUN2017', '27JUL2017', '25AUG2016']

for i in range(0, len(expiries)-2):
#{
	expiry=expiries[i]	
	expiryNext=expiries[i+1]	
	
	#get innerjoin of table for both expiries
	buyIndex = index + '_' + expiry
	sellIndex = index + '_' + expiryNext
	
	#print ('Comparing buyIndex %s, sellIndex %s' %(buyIndex, sellIndex))
	inner_join = cursor.execute('''select 
				%s.epoch, 
				%s.ltp, 
				%s.ltp 
				from 
				%s 
				INNER JOIN 
				%s ON %s.epoch = %s.epoch order by %s.epoch;''' %(buyIndex, buyIndex, sellIndex, buyIndex, sellIndex, buyIndex, sellIndex, buyIndex))

	op=0.0
	ot=''

	hp=-100000000.0
	ht=''

	lp=100000000.0
	lt=''

	cp=0.0
	ct=''

	counter = 0
	rowcount = inner_join.rowcount
	for row in inner_join:
	#{
		epoch=datetime.datetime.fromtimestamp(row[0]).strftime('%d%b%Y %H:%M')
		buyPrice=row[1]
		sellPrice=row[2]
		tp=sellPrice - buyPrice

		if(counter == 0):
			op=tp
			ot=epoch
		
		if(tp > hp):
			hp=tp
			ht=epoch

		if(tp < lp):
			lp=tp
			lt=epoch

		if(counter == (rowcount -1)):
			cp=tp
			ct=epoch

		counter += 1;
		print 'Inter Result %s-%s [op %f, ot %s]' %(buyIndex, sellIndex, tp, epoch)
	#}

	print 'Result %s-%s [op %f, ot %s] [hp %f, ht %s] [lp %f, lt %s] [cp %f, ct %s]' %(buyIndex, sellIndex, op, ot, hp, ht, lp, lt, cp, ct)
	#print('Result %s-%s [op %f, ot %s] [hp %f, ht %s] [lp %f, lt %s] [cp %f, ct %s]')
#}
	
conn.commit()
conn.close()
