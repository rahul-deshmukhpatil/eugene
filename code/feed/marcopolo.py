#!/usr/bin/python

import sqlite3
import logging

#logging.basicConfig(filename='marcopolo.log',level=logging.INFO)

def publish_future(cursor, row):
#{
	#create table
	try: 
		cursor.execute('''CREATE TABLE IF NOT EXISTS %s 
				(epoch INT PRIMARY KEY  NOT NULL,
				 bs INT NOT NULL,
				 bp REAL NOT NULL,
				 ap REAL NOT NULL,
				 ss INT NOT NULL,
				 ltp REAL NOT NULL,
				 vol INT NOT NULL,
				 total_buy INT NOT NULL,
				 total_sell INT NOT NULL,
				 oi INT NOT NULL
				);''' %(row[1]))
	except:	
		pass
	
	try:
		cursor.execute('''INSERT INTO %s
			VALUES (%d, %d, %f, %f, %d, %f, %d, %d, %d, %d)''' %(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11]))	
	except:	
		#print "Could not insert into table %s" %(row[1])
		pass
#}

def publish_option(cursor, row):
#{
	#create table
	try: 
		cursor.execute('''CREATE TABLE IF NOT EXISTS %s 
				(epoch INT PRIMARY KEY  NOT NULL,
				 bs INT NOT NULL,
				 bp REAL NOT NULL,
				 ap REAL NOT NULL,
				 ss INT NOT NULL,
				 ltp REAL NOT NULL,
				 vol INT NOT NULL,
				 oi INT NOT NULL
				);''' %(row[1]))
	except:	
		pass
	
	try:
		cursor.execute('''INSERT INTO %s
			VALUES (%d, %d, %f, %f, %d, %f, %d, %d)''' %(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]))	
	except:	
		#print "Could not insert into table %s" %(row[1])
		pass
#}

def publish_index(cursor, row):
#{
	#create table
	try: 
		cursor.execute('''CREATE TABLE IF NOT EXISTS %s 
				(epoch INT PRIMARY KEY  NOT NULL,
				 ltp REAL NOT NULL
				);''' %(row[1]))
	except:	
		pass
	
	try:
		cursor.execute('''INSERT INTO %s
			VALUES (%d, %f)''' %(row[1], row[2], row[3]))	
	except:	
		#print "Could not insert into table %s" %(row[1])
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

#}
