#!/usr/bin/python

#
#	Strategy: 
#			1> Buy one out of money bull call spread with heavier lower call option at current spot 
#			1> Buy one out of money bear put spread with heavier higher put option at current spot 
#	One Complex Strategy buy margin
#	Max Worst Risk : 80 Rs
#	Max Controlable Risk : 80 Rs
#	Max Controlable Profit : 10 Rs
#	Max Profit : 20 Rs
#	Nominal Profit
#	Max profit and risk %
###################################################################

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

for i in range(1, len(expiries)-1):
#{
	expiry=expiries[i]	
	expiry_prev=expiries[i-1]	
	
	#get index name
	buyIndex = index + '_' + expiry
	start_date_epoch = int(datetime.datetime.strptime(expiry_prev, '%d%b%Y').strftime('%s')) + 55000  
	end_date_epoch = int(datetime.datetime.strptime(expiry, '%d%b%Y').strftime('%s')) + 55000  

	buyUnd = 0;
	buyTime = '';
	sellUnd = 0;
	sellTime = '';

	#get the starting date
	#print ('Comparing buyIndex %s, sellIndex %s' %(buyIndex, sellIndex))
	inner_join = cursor.execute('''select 
				epoch, 
				underlying 
				from 
				%s 
				where epoch > %d limit 1;''' %(buyIndex, start_date_epoch))

	for row in inner_join:
		buyUnd = row[1]
		buyTime = datetime.datetime.fromtimestamp(row[0]).strftime('%d%b%Y %H:%M IST')
		#print 'Inter Result start_date [%s-%f], ' %(buyTime, buyUnd)

	inner_join = cursor.execute('''select 
				epoch, 
				underlying 
				from 
				%s;''' %(buyIndex))

	for row in inner_join:
		sellUnd = row[1]
		sellTime = datetime.datetime.fromtimestamp(row[0]).strftime('%d%b%Y %H:%M IST')
		#print 'Inter Result end_date [%s-%f], ' %(sellTime, sellUnd)

	print 'Inter Result start_date [%s-%f] end_date[%s-%f], Profit : %f' %(buyTime, buyUnd, sellTime, sellUnd, abs(sellUnd - buyUnd))
#}

	
conn.commit()
conn.close()
