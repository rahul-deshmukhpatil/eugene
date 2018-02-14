#!/usr/bin/python

from feed_yahoo_equity import *
from marcopolo_equity import *
import time
import sqlite3
import sys
import os 

if len(sys.argv) == 1:
	print "Please pass feed name as first argument !!!"
	print "./loopFeed_yahoo_equity.py [nifty50, nifty200, nifty500, midSmallCap400, nseSymbols]"
	sys.exit()

feed = sys.argv[1]

conn = sqlite3.connect('marcopoloEquity.db')
print "Opened marcopoloEquity.db database successfully";

cursor=conn.cursor()
print "Got cursor for the connection";

epoch_time = int(time.time())

#Get all symbols lists
#Get all Yahoo symbols


nifty50url = 'https://www.nseindia.com/content/indices/ind_nifty50list.csv' 
bankniftyurl = 'https://www.nseindia.com/content/indices/ind_niftybanklist.csv' 
nifty200url = 'https://www.nseindia.com/content/indices/ind_nifty200list.csv'
nifty500url = 'https://www.nseindia.com/content/indices/ind_nifty500list.csv'
midSmallCap400url = 'https://www.nseindia.com/content/indices/ind_niftymidsmallcap400list.csv'
nseSymbolsurl = 'https://www.nseindia.com/content/equities/EQUITY_L.csv'

nifty50 = get_all_nse_symbols(nifty50url); 
banknifty = get_all_nse_symbols(bankniftyurl)
nifty200 = get_all_nse_symbols(nifty200url)
nifty500 = get_all_nse_symbols(nifty500url)
midSmallCap400 = get_all_nse_symbols(midSmallCap400url)
nseSymbols = get_all_nse_symbols(nseSymbolsurl)

#print nifty50
#print banknifty
#print nifty200
#print nifty500

freq10symbols = list(set(nifty50 + banknifty))
freq60symbols = list(set(nifty200) - set(nifty50) - set(banknifty))
freq300symbols = list(set(nifty500) - set(nifty200)- set(nifty50) - set(banknifty))
freq600symbols = list(set(midSmallCap400) - set(nifty500) - set(nifty200)- set(nifty50) - set(banknifty))
freq1800symbols = list(set(nseSymbols) - set(midSmallCap400) - set(nifty500) - set(nifty200)- set(nifty50) - set(banknifty))

symbols = []

if feed == 'nifty50':
	symbols = freq10symbols
	freqtime = 10
elif feed == 'nifty200':
	symbols = freq60symbols
	freqtime = 60
elif feed == 'nifty500':
	symbols = freq300symbols
	freqtime = 300
elif feed == 'midSmallCap400':
	symbols = freq600symbols
	freqtime = 600
elif feed == 'nse':
	symbols = freq1800symbols
	freqtime = 1800
else:
	print "Wrong Feed type %s" %(feed)

if len(symbols) == 0:
	print "No symbols to feed %s" %(symbols)
	sys.exit()
else:
	print "Praying for symbosl %s" %(symbols)

#Set previous volume for all symbols = 0
prevVolume = {}
for symbol in  symbols:
	prevVolume[symbol] = 0	

while True:
	hist_data = []
	hist_data=get_yahoo_eqity_data(symbols)

	for row in hist_data:
		#publish_row_to_db_yahoo_equity(cursor, row) if it has valid epoch
		if(row[EUGENE_EPOCH] != 0):
			#Subtract prev volume
			temp = row[EUGENE_VOLUME]
			row[EUGENE_VOLUME] -= prevVolume[row[EUGENE_SYMBOL]] 
			prevVolume[row[EUGENE_SYMBOL]] = temp 
			#print "Sending to db %s" %(row)
			publish_row_to_db(cursor, row)
			conn.commit()

	epoch_time = int(time.time())
	while(epoch_time % freqtime):
		epoch_time = int(time.time())

	if os.path.exists('stop_loop_yahoo_equity.lck'):
		print 'Shutting down signal received via stop_loop_yahoo_equity.lck'
		break;

conn.close()
