import os 
import logging
import datetime  
import csv 

import eugene_expiries

logger = logging.getLogger(os.environ['logger'])

def get_start_end(frequency, date):
	if(frequency == 'daily'):
		return date, date + datetime.timedelta(1)
	elif(frequency == 'weekly'):
		return date, date + datetime.timedelta(7)
	elif(frequency == 'monthly'):
		next_month_expiry = date + datetime.timedelta(28)
		next_month_expiry_next_friday = date + datetime.timedelta(35)
		if(next_month_expiry.month != next_month_expiry_next_friday):
			return date, date + datetime.timedelta(28)
		else:
			return date, date + datetime.timedelta(35)

def run(cursor, strategy, start, end):
	#@TODO: modify start according to the current expiry
	start_date = start
	#@TODO: modify end according to the current expiry
	end_date = end

	#get underlying 
	strategy_file_handle = open(strategy, 'r')
	legs = []
	rows = csv.reader(strategy_file_handle)
	for row in rows:
		legUnderlying = row[0]
		legExpiryIndex = int(row[1])
		legCallPut = row[2]
		legSpotDiff = int(row[3])
		legBuySell = row[4]
		legRatio = float(row[5])
	
		expiry_date = eugene_expiries.get_nearest_expiry(legUnderlying, end-datetime.timedelta(1));
		nse_expiry_fmt = expiry_date.strftime('%-d%b%Y').upper()
		spotSymbol = legUnderlying + '_' + nse_expiry_fmt

		#logger.info('select ltp from %s where epoch > %d limit 1', spotSymbol, int(start_date.strftime('%s')))
		cursor.execute('''select ltp from %s where epoch > %d limit 1''' %(spotSymbol, int(start_date.strftime('%s'))))
	
		#if spot exists
		spot = 0
		rows = cursor.fetchall()
		for row in rows:
			spot = int((row[0] + 50)/100) * 100
		
		legSymbol = legUnderlying + '_' + nse_expiry_fmt + legCallPut + str(spot+legSpotDiff) 
		legs.append([legSymbol, legBuySell, legRatio])

		logger.info('Getting strike for %s : %d', spotSymbol, spot+legSpotDiff)


	sql = 'select ' + legs[0][0] + '.epoch' 
	for leg in legs:
		sql += ', ' + leg[0] + '.bp, ' + leg[0] + '.ap'

	sql += ' from ' + legs[0][0]

	for leg in legs[1:]:
		sql += ' inner join ' + leg[0] + ' on ' + leg[0] + '.epoch == ' + legs[0][0] + '.epoch'

	sql += ' where ' + legs[0][0] + '.epoch > ' + str(start_date.strftime('%s')) + ' and ' + legs[0][0] + '.epoch < ' + str(end_date.strftime('%s'))
	logger.info('SQL : %s', sql)


	cursor.execute(sql)
	rows = cursor.fetchall()

	for row in rows:
		buyPrice = 0.0
		sellPrice = 0.0
		
		legid = 1
		for leg in legs:
			#BUY the spread
			#add price at which we could buy ie ap 
			#sub price at which we could sell ie bp 
			if(leg[1] == 'B'):
				buyPrice += leg[2] * row[2*legid] 
			else:
				buyPrice -= leg[2] * row[2*legid-1] 

			#SELL the spread
			#add price at which we could sell ie bp 
			#sub price at which we could buy ie ap 
			if(leg[1] == 'B'):
				sellPrice += leg[2] * row[2*legid-1] 
			else:
				sellPrice -= leg[2] * row[2*legid] 

			legid += 1
	
		logger.info('Strategy %d] bp %f , sp %f', row[0], buyPrice, sellPrice)

def runstrategy(cursor, strategy, frequency, expiries):
	for expiry in expiries:
		start, end = get_start_end(frequency, expiry)
		logger.info('Running strat for %s - %s', start, end)
		run(cursor, strategy, start, end)
			

