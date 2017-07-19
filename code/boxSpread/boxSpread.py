#!/usr/bin/python

import time
import datetime
import sqlite3
import csv

conn = sqlite3.connect('../feed/marcopolo.db')
print "Opened database successfully";

cursor=conn.cursor()
print "Got cursor for the connection";

index='BANKNIFTY'
expiries = ['13JUL2017']

for expiry in expiries:
#{
	#get innerjoin of table for both expiries
	lowerCall = index + '_' + expiry + 'C' + '23600'
	lowerPut = index + '_' + expiry + 'P' + '23600'
	higherCall = index + '_' + expiry + 'C' + '24000'
	higherPut = index + '_' + expiry + 'P' + '24000'

	#print ('Comparing buyIndex %s, sellIndex %s' %(buyIndex, sellIndex))
	inner_join = cursor.execute('''select 
				%s.epoch, 
				%s.ap - %s.bp - %s.bp +	%s.ap,
				%s.bp - %s.ap - %s.ap +	%s.ap
				from 
				%s 
				INNER JOIN %s ON %s.epoch = %s.epoch
				INNER JOIN %s ON %s.epoch = %s.epoch
				INNER JOIN %s ON %s.epoch = %s.epoch;''' %(lowerCall, lowerCall, lowerPut, higherCall, higherPut, lowerCall, lowerPut, higherCall, higherPut, lowerCall, lowerPut, lowerCall, lowerPut, higherCall, lowerCall, higherCall, higherPut, lowerCall, higherPut))

	rowcount = inner_join.rowcount

	resultList = []

	for row in inner_join:
	#{
		rowList = []
		rowList.append(row[0]);
		rowList.append(row[1]);
		rowList.append(row[2]);
		resultList.append(rowList);
	#}

	for row in resultList[1:]:
	#{
		epoch=datetime.datetime.fromtimestamp(row[0]).strftime('%d%b%Y %H:%M')

		print 'Inter Result %s : [buy %f, sell %f]' %(epoch, row[1], row[2])
		
	#}

	#print('Result %s-%s [op %f, ot %s] [hp %f, ht %s] [lp %f, lt %s] [cp %f, ct %s]')
#}
	
conn.commit()
conn.close()
