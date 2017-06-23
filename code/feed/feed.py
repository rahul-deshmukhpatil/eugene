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

expiry_url = 'https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?date=-&instrument=-&symbol='
option_url = 'https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?'
option_site = 'https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?symbol=&lt;symbol&gt;&amp;date=&lt;expiry&gt;&amp;instrument=&lt;imnt_type&gt;'  

future_url="https://www.nseindia.com/live_market/dynaContent/live_watch/fomwatchsymbol.jsp?Fut_Opt=Futures"
future_index_expiry_url="https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuoteFO.jsp?instrument=FUTIDX"

# Gets quotes for the expiry of the 
# STRIKES for symbol 
#########################################
def get_option_chain_for_expiry(symbol, expiry):
#{
	url = option_url + 'symbol=' + symbol + '&date=' + expiry;
	#logging.info('Getting Option Chain for SYMBOL:%s EXPIRY:%s URL:%s', symbol, expiry, url)

	expiry_page=get_url(url)
	#logging.debug('Response Start:\n%s\nResponse End', expiry_page)

	bs4obj = BeautifulSoup(expiry_page)
	table = bs4obj.findAll('table', {'id' : 'octable'})[0]
	rows = table.findAll('tr')  
	
	undSpot=int(float(re.sub(r".* ", "", bs4obj.findAll('span')[0].getText())))
	time=int(datetime.datetime.strptime(re.sub(r"As on ", "", bs4obj.findAll('span')[1].getText()), '%b %d, %Y %H:%M:%S IST ').strftime('%s'))
	#logging.info('Spot:%s Time:%d', undSpot, time)

	index=1
	for row in rows[2:-1]:
	#{
		#logging.debug('%d] Option Chain row for SYMBOL:%s EXPIRY:%s', index, symbol, expiry)
		index += 1
		fields=row.findAll('td')
	
		STRIKE = int(float(fields[F_STRIKE].getText()))
		
		try:
			cf_bs = int(fields[CF_BS].getText().replace(',',''))
			cf_bp = float(fields[CF_BP].getText().replace(',',''))
			cf_ap = float(fields[CF_AP].getText().replace(',',''))
			cf_as = int(fields[CF_AS].getText().replace(',',''))
			#logging.info('Option Chain row for SYMBOL:%s EXPIRY:%s STRIKE: %d CALL: [%d, %f, %f, %d]', symbol, expiry, STRIKE, cf_bs, cf_bp, cf_ap, cf_as)
		except ValueError:
			#logging.error('Invalid Option Chain row for SYMBOL:%s EXPIRY:%s STRIKE: %d CALL', symbol, expiry, STRIKE)
			pass

		try:
			pf_bs = int(fields[PF_BS].getText().replace(',',''))
			pf_bp = float(fields[PF_BP].getText().replace(',',''))
			pf_ap = float(fields[PF_AP].getText().replace(',',''))
			pf_as = int(fields[PF_AS].getText().replace(',',''))
			#logging.info('Option Chain row for SYMBOL:%s EXPIRY:%s STRIKE: %d PUT : [%d, %f, %f, %d]', symbol, expiry, STRIKE, pf_bs, pf_bp, pf_ap, pf_as)
		except ValueError:
			#logging.error('Invalid Option Chain row for SYMBOL:%s EXPIRY:%s STRIKE: %d PUT', symbol, expiry, STRIKE)
			pass
	#}
#}

# Gets quotes for the all particular expiry of future
# for the symbol
#########################################
def get_futures_quote_for_expiry(symbol, expiry):
#{
	#get the future data
	url = future_index_expiry_url + '&underlying=' + symbol + '&expiry=' + expiry
	future_page=get_url(url)
	#logging.info('Gettting future data for UND:%s EXPIRY:%s URL:%s', symbol, expiry, url)
	
	bs4obj = BeautifulSoup(future_page)

	linesList=bs4obj.findAll('div', {'id' : 'responseDiv'})[0].getText().splitlines()
	validLine = [x for x in linesList if "valid" in x]

	#logging.info('Response Quotes List  Start:\n%s\nResponse End', validLine[0])
	quotesList = json.loads(validLine[0])['data']
	quotesDict = quotesList[0] 

	logging.info('Response Quotes Dict Start:\n%s\nResponse End', quotesDict)
#}

# Gets quotes for the all expiries of future
# for the symbol
#########################################
def get_futures_chain(symbol):
#{
	#get the future data
	url = future_url + '&key=' + symbol;
	future_page=get_url(url)
	bs4obj = BeautifulSoup(future_page)
	table = bs4obj.findAll('table')[1]
	#logging.debug('Response Start:\n%s\nResponse End', future_page)

	rows = table.findAll('tr')  
	
	#undSpot=int(float(re.sub(r".* ", "", bs4obj.findAll('span')[0].getText())))
	#time=int(datetime.datetime.strptime(re.sub(r".*As on ", "", bs4obj.findAll('td')[1].getText()), '%b %d, %Y %H:%M:%S IST ').strftime('%s'))
	#logging.info('Spot:%s Time:%d', undSpot, time)

	for row in rows[1:]:
		fields=row.findAll('td')
		expiry=fields[2].getText()
		date=get_date(expiry)
		if date:
		#{
			#logging.info('UND:%s, EXPIRY %s', symbol, expiry.getText())
			get_futures_quote_for_expiry(symbol, expiry)
			pass
		#}
#}


# Gets quotes for the MAX_EXPIRIES of the 
# STRIKES for symbol 
#########################################
def get_option_chain(symbol):
#{
	#get the future data
	get_futures_chain(symbol)

	url = option_url + 'symbol=' + symbol;
	#logging.info('Getting Expiries for SYMBOL:%s URL:%s', symbol, url)

	expiry_page=get_url(url)
	#logging.debug('Response Start:\n%s\nResponse End', expiry_page)

	index = 1
	bs4obj = BeautifulSoup(expiry_page)

	expiries = bs4obj.findAll('select', {'id' : 'date'})[0]
	expiryDates=[]

   	for expiry in expiries.findChildren('option'):  
	#{
		date=get_date(expiry.getText())

		if date:
		#{
			#logging.info('%d] UND:%s, EXPIRY %s', index, symbol, expiry.getText())
			expiryDates.append(expiry.getText());
			index += 1;
		#}
	#}

	for expiry in expiryDates[0:MAX_EXPIRIES]:
	#{
		#logging.info('Getting data for chain UND:%s, EXPIRY %s', symbol, expiry)
		get_option_chain_for_expiry(symbol, expiry)
	#}

#}


logging.basicConfig(filename='example.log',level=logging.INFO)

def main():
	symbols = ['NIFTY', 'BANKNIFTY']
	for symbol in symbols:
		get_option_chain(symbol)

main()

