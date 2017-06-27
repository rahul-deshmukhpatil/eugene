#!/usr/bin/python

from feed import *
from marcopolo import *
import sqlite3

conn = sqlite3.connect('marcopolo')
print "Opened database successfully";

cursor=conn.cursor()
print "Got cursor for the connection";

hist_data=get_option_future_data()
#cursor.execute('''CREATE TABLE simple1 
#		(epoch INT NOT NULL,
#		 bs INT NOT NULL,
#		 bp REAL NOT NULL,
#		 ap REAL NOT NULL,
#		 ss INT NOT NULL,
#		 lp REALNOT NULL,
#		 vol INT NOT NULL,
#		 total_buy INT NOT NULL,
#		 total_sell INT NOT NULL,
#		 oi INT NOT NULL
#		);''')

for row in hist_data:
	publish_row_to_db(cursor, row)
	conn.commit()

conn.close()
