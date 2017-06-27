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
	epoch=int(datetime.datetime.strptime(re.sub(r"As on ", "", bs4obj.findAll('span')[1].getText()), '%b %d, %Y %H:%M:%S IST ').strftime('%s'))
	#logging.info('Spot:%s Time:%d, Table Rows %d', undSpot, epoch, len(rows))

	strikeMin = undSpot - STRIKE_SPREAD;
	strikeMax = undSpot + STRIKE_SPREAD;

	hist_data = []
	hist_data.append(['STOCK', symbol, epoch, undSpot])

	index=1
	for row in rows[2:-1]:
	#{
		index += 1
		fields=row.findAll('td')

		#Only options around 600 points of the underlying and multiple of 100
		STRIKE = int(float(fields[F_STRIKE].getText()))

		if(STRIKE < strikeMin):
			continue

		if(STRIKE > strikeMax):
			continue
		
		if(STRIKE % 100):
			continue

		#logging.info('%d] Option Chain row for SYMBOL:%s EXPIRY:%s STRIKE:%d', index, symbol, expiry, STRIKE)
		
		try:
			cf_oi = int(fields[CF_OI].getText().replace(',',''))
			#cf_change_oi = int(fields[CF_CHANGE_OI].getText().replace(',',''))
			cf_volume = int(fields[CF_VOLUME].getText().replace(',',''))
			#cf_iv = int(fields[CF_IV].getText().replace(',',''))
			cf_ltp = float(fields[CF_LTP].getText().replace(',',''))
			#cf_net_change = float(fields[CF_NETCHANGE].getText().replace(',',''))
			cf_bs = int(fields[CF_BS].getText().replace(',',''))
			cf_bp = float(fields[CF_BP].getText().replace(',',''))
			cf_ap = float(fields[CF_AP].getText().replace(',',''))
			cf_as = int(fields[CF_AS].getText().replace(',',''))
			#logging.info('Option Chain row for SYMBOL:%s EXPIRY:%s STRIKE: %d CALL: [%d, %f, %f, %d]', symbol, expiry, STRIKE, cf_bs, cf_bp, cf_ap, cf_as)
			hist_data.append(['OPTION', symbol + '_' + expiry + 'C' + str(STRIKE), epoch, cf_bs, cf_bp, cf_ap, cf_as, cf_ltp, cf_volume, cf_oi])
		except ValueError:
			#logging.error('Invalid Option Chain row for SYMBOL:%s EXPIRY:%s STRIKE: %d CALL', symbol, expiry, STRIKE)
			pass

		try:
			pf_oi = int(fields[PF_OI].getText().replace(',',''))
			#pf_change_oi = int(fields[PF_CHANGE_OI].getText().replace(',',''))
			pf_volume = int(fields[PF_VOLUME].getText().replace(',',''))
			#pf_iv = int(fields[PF_IV].getText().replace(',',''))
			pf_ltp = float(fields[PF_LTP].getText().replace(',',''))
			#pf_net_change = int(fields[PF_NETCHANGE].getText().replace(',',''))
			pf_bs = int(fields[PF_BS].getText().replace(',',''))
			pf_bp = float(fields[PF_BP].getText().replace(',',''))
			pf_ap = float(fields[PF_AP].getText().replace(',',''))
			pf_as = int(fields[PF_AS].getText().replace(',',''))
			#logging.info('Option Chain row for SYMBOL:%s EXPIRY:%s STRIKE: %d PUT : [%d, %f, %f, %d]', symbol, expiry, STRIKE, pf_bs, pf_bp, pf_ap, pf_as)
			hist_data.append(['OPTION', symbol + '_' + expiry + 'P' + str(STRIKE), epoch, pf_bs, pf_bp, pf_ap, pf_as, pf_ltp, pf_volume, pf_oi])
		except ValueError:
			#logging.error('Invalid Option Chain row for SYMBOL:%s EXPIRY:%s STRIKE: %d PUT', symbol, expiry, STRIKE)
			pass
	#}
	return hist_data
#}

# Gets quotes for the all particular expiry of future
# for the symbol
#########################################
def get_futures_quote_for_expiry(symbol, expiry):
#{
	hist_data = []

	#get the future data
	url = future_index_expiry_url + '&underlying=' + symbol + '&expiry=' + expiry
	future_page=get_url(url)
	#logging.info('Gettting future data for UND:%s EXPIRY:%s URL:%s', symbol, expiry, url)
	
	bs4obj = BeautifulSoup(future_page)

	linesList=bs4obj.findAll('div', {'id' : 'responseDiv'})[0].getText().splitlines()
	validLine = [x for x in linesList if "valid" in x]

	#logging.info('Response Quotes List  Start:\n%s\nResponse End', validLine[0])
	line = json.loads(validLine[0])
	quotesList = line['data']
	futureDict = quotesList[0] 

	#logging.info('Response Quotes Dict Start:\n%s\nResponse End', quotesDict)
	epoch=int(datetime.datetime.strptime(line['lastUpdateTime'], '%d-%b-%Y %H:%M:%S').strftime('%s'))

	bs = int(futureDict['buyQuantity1'].replace(',',''))
	bp = float(futureDict['buyPrice1'].replace(',',''))
	sp = float(futureDict['sellPrice1'].replace(',',''))
	ss = int(futureDict['sellQuantity1'].replace(',',''))
	lastPrice = float(futureDict['lastPrice'].replace(',','')) 
	vol = int(futureDict['numberOfContractsTraded'].replace(',',''))
	total_buy = int(futureDict['totalBuyQuantity'].replace(',',''))
	total_sell = int(futureDict['totalSellQuantity'].replace(',',''))
	oi = int(futureDict['openInterest'].replace(',',''))

	hist_data.append(['FUTURE', symbol + '_' + expiry, epoch, bs, bp, sp, ss, lastPrice, vol, total_buy, total_sell, oi]);
	return hist_data
#}

# Gets quotes for the all expiries of future
# for the symbol
#########################################
def get_futures_chain(symbol):
#{
	hist_data = []
	#get the future data
	url = future_url + '&key=' + symbol;
	future_page=get_url(url)
	bs4obj = BeautifulSoup(future_page)
	table = bs4obj.findAll('table')[1]
	#logging.debug('Response Start:\n%s\nResponse End', future_page)

	rows = table.findAll('tr')  
	
	for row in rows[1:]:
		fields=row.findAll('td')
		expiry=fields[2].getText()
		date=get_date(expiry)
		if date:
		#{
			#logging.info('UND:%s, EXPIRY %s', symbol, expiry.getText())
			hist_data = hist_data + get_futures_quote_for_expiry(symbol, expiry)
			pass
		#}

	return hist_data
#}


# Gets quotes for the MAX_EXPIRIES of the 
# STRIKES for symbol 
#########################################
def get_option_chain(symbol):
#{
	hist_data = []

	#get the future data
	hist_data = hist_data + get_futures_chain(symbol)

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
		option_chain=get_option_chain_for_expiry(symbol, expiry)
		hist_data = hist_data + option_chain
	#}

	return hist_data
#}


logging.basicConfig(filename='feed.log',level=logging.INFO)

def get_option_future_data():
	symbols = ['NIFTY', 'BANKNIFTY']
	hist_data = []
	for symbol in symbols:
		option_chain=get_option_chain(symbol)
		hist_data = hist_data + option_chain
	
	return hist_data

#main()

