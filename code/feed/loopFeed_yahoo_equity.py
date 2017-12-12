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


while True:
	print "Getting Data for %d" %(epoch_time)

	symbols = get_all_nse_symbols()
	hist_data=get_yahoo_eqity_data(symbols)

	for row in hist_data:
		#publish_row_to_db_yahoo_equity(cursor, row)
		conn.commit()

	epoch_time = int(time.time())
	while(epoch_time % 60):
		epoch_time = int(time.time())

	if os.path.exists('stop_loop_yahoo_equity.lck'):
		break;

conn.close()
