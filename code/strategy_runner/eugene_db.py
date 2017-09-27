import sqlite3
import logging
import os 

logger = logging.getLogger(os.environ['logger'])

def open_db():
	db_path='../feed/marcopolo.db'

	conn = sqlite3.connect(db_path)

	cursor=conn.cursor()
	logger.info('Got cursor for the connection : %s', db_path)
	logger.info('Opened database successfully : %s', db_path)
	
	return cursor;

