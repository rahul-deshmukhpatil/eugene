#!/usr/bin/python

from feed_yahoo_equity import *
from marcopolo_equity import *
import time
import sqlite3

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

while True:
	print "Getting Data for %d" %(epoch_time)

	nifty50 = get_all_nse_symbols(nifty50url); 
	banknifty = get_all_nse_symbols(bankniftyurl)
	nifty200 = get_all_nse_symbols(nifty200url)
	nifty500 = get_all_nse_symbols(nifty500url)

	#print nifty50
	#print banknifty
	#print nifty200
	#print nifty500


	freq10symbols = list(set(nifty50 + banknifty))
	freq60symbols = list(set(nifty200) - set(freq10symbols))
	freq180symbols = list(set(nifty500) - set(nifty200url))
	hist_data=get_yahoo_eqity_data(freq180symbols)

	for row in hist_data:
		#publish_row_to_db_yahoo_equity(cursor, row)
		conn.commit()

	epoch_time = int(time.time())
	while(epoch_time % 60):
		epoch_time = int(time.time())

	if os.path.exists('stop_loop_yahoo_equity.lck'):
		break;

conn.close()
