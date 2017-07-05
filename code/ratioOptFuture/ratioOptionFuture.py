#!/usr/bin/python

import time
import datetime
import sqlite3
import csv

conn = sqlite3.connect('../feed/marcopolo.db')
print "Opened database successfully";

cursor=conn.cursor()
print "Got cursor for the connection";

index='NIFTY'
expiries = ['27JUL2017']

for expiry in expiries:
#{
	#get innerjoin of table for both expiries
	sellIndex = index + '_' + expiry
	buyCall = index + '_' + expiry + 'C9700'
	
	#print ('Comparing buyIndex %s, sellIndex %s' %(buyIndex, sellIndex))
	inner_join = cursor.execute('''select 
				%s.epoch, 
				%s.bp, 
				%s.ap,
				%s.bp, 
				%s.ap
				from 
				%s 
				INNER JOIN 
				%s ON %s.epoch = %s.epoch order by %s.epoch;''' %(sellIndex, sellIndex, sellIndex, buyCall, buyCall, sellIndex, buyCall, sellIndex, buyCall, sellIndex))

	#strategy buy and sell price and time
	obp=0.0
	osp=0.0
	ot=''

	counter = 0
	rowcount = inner_join.rowcount

	resultList = []

	for row in inner_join:
	#{
		rowList = []
		rowList.append(row[0]);
		rowList.append(row[1]);
		rowList.append(row[2]);
		rowList.append(row[3]);
		rowList.append(row[4]);
		resultList.append(rowList);
	#}

	for row in resultList[1:]:
	#{
		epoch=datetime.datetime.fromtimestamp(row[0]).strftime('%d%b%Y %H:%M')

		#If you want to buy strategy
		# buy call and sell index
		indexBuyPrice=resultList[0][1]
		optionSellPrice=resultList[0][4]
		#obp = indexBuyPrice - (2 * optionSellPrice) - 9000

		#sell the strategy
		# sell call and buy index
		indexSellPrice=row[2]
		optionBuyPrice=row[3]
		#osp= indexSellPrice - 2 * (optionBuyPrice) - 9000

		profit = indexSellPrice - indexBuyPrice + ( 2 * (optionSellPrice - optionBuyPrice) )

		print 'Inter Result %s-%s [%s [%f - %f] - [%f - %f] %f]' %(sellIndex, buyCall, epoch, indexBuyPrice, optionSellPrice, indexSellPrice, optionBuyPrice, profit)
		
	#}

	#print('Result %s-%s [op %f, ot %s] [hp %f, ht %s] [lp %f, lt %s] [cp %f, ct %s]')
#}
	
conn.commit()
conn.close()
