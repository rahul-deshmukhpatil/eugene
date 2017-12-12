#!/bin/python

import sys 
import json 
import datetime  
import logging
import re 
from bs4 import BeautifulSoup  

from geturl import * 
from reftypes import * 
from utils import * 
from multiprocessing import Pool


equity_url="https://finance.yahoo.com/quote/"


# Gets quotes for the MAX_EXPIRIES of the 
# STRIKES for symbol 
#########################################
def get_symbol_data_from_yahoo(symbol):
#{
	url = equity_url + symbol + '.NS'
	logging.info('Getting Expiries for SYMBOL:%s URL:%s', symbol, url)
	print url

	hist_data = [None] * EUGENE_MAX

	equity_page = None
	while equity_page is None:
		try:
			#Get page, Sometimes returns None 
			equity_page = get_url(url)
		except:
			pass

	bs4obj = BeautifulSoup(equity_page, "html.parser")

	#Extracting json objects
	script = bs4obj.find("script",text=re.compile("root.App.main")).text
	jsonData = json.loads(re.search("root.App.main\s+=\s+(\{.*\})", script).group(1))
	stores = jsonData["context"]["dispatcher"]["stores"]

	hist_data[EUGENE_SEC_TYPE]	= 'STOCK'
	hist_data[EUGENE_SYMBOL] 	= symbol 
	hist_data[EUGENE_EPOCH]		= 0
	hist_data[EUGENE_VOLUME] 	= stores[u'QuoteSummaryStore'] [u'summaryDetail'] ['volume']['raw'] 
	try:
		hist_data[EUGENE_LTP] = stores[u'QuoteSummaryStore'] [u'financialData'] [u'currentPrice']['raw']
	except:
		hist_data[EUGENE_LTP] = stores[u'QuoteSummaryStore'] [u'price'] [u'regularMarketPrice']['raw']
	print hist_data 
	return hist_data
#}


logging.basicConfig(filename='feed.log',level=logging.INFO)

def get_yahoo_eqity_data(symbols):
	symbols1 = ['BIOCON'
, 'ADANIPORTS'
, 'AMBUJACEM'
, 'ASIANPAINT'
, 'AUROPHARMA'
, 'AXISBANK'
, 'BAJAJ-AUTO'
, 'BAJFINANCE'
, 'BPCL'
, 'BHARTIARTL'
, 'INFRATEL'
, 'BOSCHLTD'
, 'CIPLA'
, 'COALINDIA'
, 'DRREDDY'
, 'EICHERMOT'
, 'GAIL'
, 'HCLTECH'
, 'HDFCBANK'
, 'HEROMOTOCO'
, 'HINDALCO'
, 'HINDPETRO'
, 'HINDUNILVR'
, 'HDFC'
, 'ITC'
, 'ICICIBANK'
, 'IBULHSGFIN'
, 'IOC'
, 'INDUSINDBK'
, 'INFY'
, 'KOTAKBANK'
, 'LT'
, 'LUPIN'
, 'M&M'
, 'MARUTI'
, 'NTPC'
, 'ONGC'
, 'POWERGRID'
, 'RELIANCE'
, 'SBIN'
, 'SUNPHARMA'
, 'TCS'
, 'TATAMOTORS'
, 'TATASTEEL'
, 'TECHM'
, 'UPL'
, 'ULTRACEMCO'
, 'VEDL'
, 'WIPRO'
, 'YESBANK'
, 'ZEEL']
	hist_data = []
	#for symbol in symbols:
		#symbol_data = get_symbol_data_from_yahoo(symbol)
		#hist_data = hist_data + symbol_data 
	mp = Pool(51)
	mp.map(get_symbol_data_from_yahoo, symbols)
	mp.close()
	mp.join()

	sys.exit()
	return hist_data

import csv
import StringIO

# Get all symbols on the NSE 
#########################################
def get_all_nse_symbols():
#{
	symbols_file = get_url('https://www.nseindia.com/content/equities/EQUITY_L.csv')
	symbols_file = csv.reader(StringIO.StringIO(symbols_file))
	symbols = []
	for symbol in symbols_file:
		symbols.append(symbol[0])
	return symbols[1:] 
#}


#main()
