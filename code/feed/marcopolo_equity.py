#!/usr/bin/python

import sqlite3
import logging
from reftypes import * 

#logging.basicConfig(filename='marcopolo.log',level=logging.INFO)

masterTable='masterT'

def publish_stock(cursor, row):
#{
	#create table
	try: 
		cursor.execute('''CREATE TABLE IF NOT EXISTS %s 
				(
				 product TEXT NOT NULL,
				 symbol TEXT NOT NULL,
				 updateType TEXT NOT NULL,
				 epoch INT NOT NULL,
				 ltp REAL NOT NULL,
				 volume INT
				);''' %(masterTable))
	except:	
		print "Could not create table : %s" %(masterTable)
		pass
	
	try:
		cursor.execute('''INSERT INTO %s
			VALUES (%s, %s, %s, %d, %f, %d)''' %(masterTable, row[EUGENE_SEC_TYPE], row[EUGENE_SYMBOL], row[EUGENE_UPDATE], row[EUGENE_EPOCH], row[EUGENE_LTP], row[EUGENE_VOLUME]))	
	except:	
		print "Could not insert into table %s: %s" %(masterTable, row)
		pass
#}


def publish_row_to_db(cursor, row):
#{
	if row[0] == 'FUTURE':
		publish_future(cursor, row);
	elif row[0] == 'OPTION':
		publish_option(cursor, row);
	elif row[0] == 'INDEX':
		publish_index(cursor, row);
	elif row[EUGENE_SEC_TYPE].upper() == 'STOCK':
		publish_stock(cursor, row);
#}
