import os 
import logging
import datetime  
import csv 
import time 

import eugene_expiries
import eugene_exception

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

def get_exact_leg_definions(cursor, strategy, start_date, end_date, entry_delta, exit_delta):
	#get underlying 
	strategy_file_handle = open(strategy, 'r')
	legs = []
	rows = csv.reader(strategy_file_handle)

	underlyings = []

	for row in rows:
		legUnderlying = row[0]
		legExpiryIndex = int(row[1])
		legCallPut = row[2]
		legSpotDiff = int(row[3])
		legBuySell = row[4]
		legRatio = float(row[5])

		#add underlying to set
		if legUnderlying not in underlyings:
			underlyings.append(legUnderlying)

		#logger.info('select ltp from %s where epoch > %d limit 1', spotSymbol, int(start_date.strftime('%s')))
		if(entry_delta):
			entry_date = end_date - datetime.timedelta(entry_delta)
		else:
			entry_date = start_date

		cursor.execute('''select ltp from %s where epoch > %d limit 1''' %(legUnderlying, int(entry_date.strftime('%s'))))
	
		#if spot exists
		spot = 0
		rows = cursor.fetchall()
		for row in rows:
			spot = int((row[0] + 50)/100) * 100

		if spot == 0:
			raise NoSpotForDay(entry_date)

		nse_expiry_fmt = ''
		exact_spot = str(spot+legSpotDiff) 
		
		logger.info("Entry Date %s, Spot is %d, SpotDelta is %d, exact spot %s", end_date, spot, legSpotDiff, exact_spot);

		if not legCallPut:
			exact_spot = ''
			nse_expiry_fmt = eugene_expiries.nearest_expiry(False, legUnderlying, legExpiryIndex, (end_date - datetime.timedelta(1))).strftime('%-d%b%Y').upper()
		else:	
			nse_expiry_fmt = eugene_expiries.nearest_expiry(True, legUnderlying, legExpiryIndex, (end_date - datetime.timedelta(1))).strftime('%-d%b%Y').upper()

		legSymbol = legUnderlying + '_' + nse_expiry_fmt + legCallPut + exact_spot 

		legDetailedSymbol = legSymbol + '-' + legBuySell + '-' + str(legRatio)
		legs.append([legSymbol, legBuySell, legRatio, legDetailedSymbol])
	
	return legs, underlyings

def get_sql_command(legs, underlyings, start_date, end_date, entry_delta, exit_delta):
	base_underlying = underlyings[0]
	sql = 'select ' + base_underlying + '.epoch, ' + base_underlying + '.ltp' 

	for underlying in underlyings[1:]:
		sql += ', ' + underlying + '.ltp' 

	for leg in legs:
		sql += ', ' + leg[0] + '.bp, ' + leg[0] + '.ap'

	sql += ' from ' + base_underlying 

	for underlying in underlyings[1:]:
		sql += ' inner join ' + underlying + ' on ' + base_underlying + '.epoch == ' + underlying + '.epoch'

	for leg in legs:
		sql += ' inner join ' + leg[0] + ' on ' + base_underlying + '.epoch == ' + leg[0] + '.epoch'

	if(entry_delta):
		entry_date = end_date - datetime.timedelta(entry_delta)
	else:
		entry_date = start_date

	exit_date = end_date - datetime.timedelta(exit_delta)

	sql += ' where ' + base_underlying + '.epoch > ' + str(entry_date.strftime('%s')) + ' and ' + base_underlying + '.epoch < ' + str(exit_date.strftime('%s'))
	logger.info('SQL : %s', sql)

	return sql

def get_strategy_symbol(legs):
	strategy_symbol = ''
	underscore = ''
	for leg in legs:
		strategy_symbol += underscore + leg[3] 
		underscore = '_'

	return strategy_symbol

def calculate_real_time_buy_sell_price(strategy_symbol, underlyings, legs, row):
	offset = 1 + len(underlyings)
	buyPrice = 0.0
	sellPrice = 0.0
	legId = 0
	underlyingId = 0
	price_string = ''

	for underlying in underlyings:
		price_string += underlying + ':[' + str(row[underlyingId + 1]) + '] '
		underlyingId += 1


	for leg in legs:
		#BUY the spread
		#add price at which we could buy ie ap 
		#sub price at which we could sell ie bp 
		if(leg[1] == 'B'):
			buyPrice += leg[2] * row[offset + 2*legId+1] 
		else:
			buyPrice -= leg[2] * row[offset + 2*legId] 

		#SELL the spread
		#add price at which we could sell ie bp 
		#sub price at which we could buy ie ap 
		if(leg[1] == 'B'):
			sellPrice += leg[2] * row[offset + 2*legId] 
		else:
			sellPrice -= leg[2] * row[offset + 2*legId + 1] 

		price_string += leg[0] + ':[' + str(row[offset + 2*legId]) + ',' + str(row[offset + 2*legId+1]) + ']'
		legId += 1
	

	return price_string, buyPrice, sellPrice
	#logger.info('%s %s - %d] %s', strategy_symbol , time.strftime("%Y/%m/%d, %H:%M:%S", time.localtime(row[0])), row[0], price_string)
	#logger.info('%s %s - %d] bp %f , sp %f', strategy_symbol , time.strftime("%Y/%m/%d, %H:%M:%S", time.localtime(row[0])), row[0], buyPrice, sellPrice)

def calculate_buy_sell_price(strategy_symbol, underlyings, legs, rows):
	# Add 1 for epoch and no of underlyings to get first leg bp, ap

	for row in rows:
		price_string, buyPrice, sellPrice = calculate_real_time_buy_sell_price(strategy_symbol, underlyings, legs, row)

		logger.info('%s %s - %d]', strategy_symbol , time.strftime("%Y/%m/%d, %H:%M:%S", time.localtime(row[0])), row[0])
		logger.info('%s', price_string)
		logger.info('====> %s] bp %f , sp %f', time.strftime("%Y/%m/%d, %H:%M:%S", time.localtime(row[0])), buyPrice, sellPrice)
		logger.info('')

def run(cursor, strategy, start, end, entry_delta, exit_delta):
	#@TODO: modify start according to the current expiry
	start_date = start
	#@TODO: modify end according to the current expiry
	end_date = end

	legs, underlyings = get_exact_leg_definions(cursor, strategy, start, end, entry_delta, exit_delta) 

	sql = get_sql_command(legs, underlyings, start_date, end_date, entry_delta, exit_delta)

	strategy_symbol = get_strategy_symbol(legs)

	cursor.execute(sql)
	rows = cursor.fetchall()

	calculate_buy_sell_price(strategy_symbol, underlyings, legs, rows)

def runstrategy(cursor, strategy, frequency, expiries, entry_delta, exit_delta):
	for expiry in expiries:
		start, end = get_start_end(frequency, expiry)
		logger.info('Running strat for %s - %s', start, end)
		try:
			run(cursor, strategy, start, end, entry_delta, exit_delta)
		except eugene_exception.NoSpotForDay as ns:
			logger.error('%s', ns.log())
		except:
			logger.error('UNKNOWN EXCPETION')

