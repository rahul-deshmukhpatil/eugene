#!/usr/bin/python

import time
import datetime
import sqlite3
import csv
import math

conn = sqlite3.connect('../feed/marco.db')
print "Opened database successfully";

cursor=conn.cursor()
print "Got cursor for the connection";

index='NIFTY'
expiries = ['27JUL2017']
index_tick=100
days_to_test=40

index='BANKNIFTY'
expiries = ['20JUL2017']
index_tick=100
days_to_test=10

for expiry in expiries:
#{
	#get the expiry day
	expiryDate = datetime.datetime.strptime(expiry, '%d%b%Y')
	dates = [expiryDate - datetime.timedelta(x) for x in reversed(range(0, days_to_test))]

	for  date in dates:
		#print "For expiry %s : %s  %s" %(expiry, expiryDate, date)
		
		#get the first spot price at 9:30 
		nineFifteen = int(date.strftime('%s')) + 32400 + 900;
		ten			= int(date.strftime('%s')) + 36000;
		closeTime	= int(date.strftime('%s')) + 54900;
 

		#get the spot at 10
		spotSymbol = index + '_' + expiry
		spotSymbol = index + '_' + '27JUL2017' 
	
		cursor.execute('''select ltp,epoch from %s where epoch > %d and epoch < %d;''' %(spotSymbol, nineFifteen, ten))

		spot = 0
		spotTime = 0
		
		#if spot exists
		if cursor.fetchone():
			row = cursor.fetchone()
			spot = row[0]
			spotTime = row[1]

			lowerIndex = math.floor((spot)/index_tick) * index_tick
			higherIndex = math.ceil((spot)/index_tick) * index_tick 

			reminder = spot % index_tick

			if reminder < (index_tick/2):
				lowerIndex = lowerIndex - index_tick
			
			if reminder > (index_tick/2):
				higherIndex = higherIndex + index_tick
			
			#higher index to buy 
			call = index + '_' + expiry + 'C' + str(int(lowerIndex))
			put = index + '_' + expiry + 'P' + str(int(higherIndex))

			cursor.execute('''select datetime(%s.epoch, 'unixepoch', 'localtime'), %s.bp+ %s.bp, %s.ap + %s.ap from %s inner join %s on %s.epoch == %s.epoch where %s.epoch > %d and %s.epoch < %d;''' %(call, call, put, call, put, call, put, call, put, call, nineFifteen, call, closeTime))

			#print "For expiry %s : On %s Running strategy for [%d-%d] spot=%d range[%d:%d]" %(expiry, date, nineFifteen, ten, spot, lowerIndex, higherIndex)

			high = 0.0
			highTime = ''
			low = 10000000000.0
			lowTime = ''

			for row in cursor:
				print "For expiry %s : On %s strategy Time %s [sell:%f buy:%f]" %(index + '_' + expiry, date, row[0], row[1], row[2])

				if row[1] > high:
					high = row[1]
					highTime = row[0]

				if row[2] < low:
					low = row[2]
					lowTime = row[0]

			print " "
			print "Summery: indexpair [%f-%f] best sell [%s %f] 	best buy [%s %f]" %(lowerIndex, higherIndex, highTime, high, lowTime, low)	
			print " "

#}
	
conn.commit()
conn.close()
