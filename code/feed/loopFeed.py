#!/usr/bin/python

from feed import *
from marcopolo import *
import time
import sqlite3

conn = sqlite3.connect('marcopolo.db')
print "Opened database successfully";

cursor=conn.cursor()
print "Got cursor for the connection";

epoch_time = int(time.time())

while True:
	print "Getting Data for %d" %(epoch_time)
	hist_data=get_option_future_data()

	for row in hist_data:
		publish_row_to_db(cursor, row)
		conn.commit()

	epoch_time = int(time.time())
	while(epoch_time % 60):
		epoch_time = int(time.time())

	if os.path.exists('stop_loop.lck'):
		break;

conn.close()
