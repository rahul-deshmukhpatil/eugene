import os 
import datetime  
import logging

logger = logging.getLogger(os.environ['logger'])

#
# 	date : date with which we have to calculate next weekly/monthly
#		expiry is being calculated
# 
#	legExpiryIndex : 0 = next expiry
#					 1 = next to next expiry
###################################################
def nearest_expiry(underlying, legExpiryIndex, date):
	#get the nearest thursday
	expiry = ''

	if(underlying == 'BANKNIFTY'):
		if(date.weekday() > 3):
			expiry = date + datetime.timedelta(7-date.weekday()+3)
		else:
			expiry = date + datetime.timedelta(3-date.weekday())
	else:
		month_start, month_end = calendar.monthrange(date.year, date.month)
		month_end = datetime.datetime(date.year, date.month, month_end)
		if(month_end.weekday() >= 3):
			month_end = month_end - datetime.timedelta(month_end.weekday()-3)
		else:
			month_end = month_end - datetime.timedelta(0-month_end.weekday()-4)

		#date is after last thursday of month so go to next month
		if(date > month_end):
			expiry = nearest_expiry(date + datetime.timedelta(8))
		else:
			expiry = month_end

	#if legExpiryIndex is not 0, calculate the next expiry
	if(legExpiryIndex > 0):
		return nearest_expiry(underlying, legExpiryIndex-1, expiry + datetime.timedelta(1))
	else:
		return expiry

def get_expiries(frequency, start_date, end_date):
	start = datetime.datetime.strptime(start_date, '%d%b%Y')
	end = datetime.datetime.strptime(end_date, '%d%b%Y')

	dates = []
	days = (end - start).days + 1

	if(frequency == 'daily'):
		dates = [start + datetime.timedelta(days=x) for x in range(0, days)]
	elif(frequency == 'weekly'):
		for x in range(0, days):
			temp_date = start + datetime.timedelta(x)
			if(temp_date.weekday() == 4):
				dates.append(temp_date)
	elif(frequency == 'monthly'):
		for x in range(0, days):
			temp_date = start + datetime.timedelta(x)

			if(temp_date.weekday() == 4):
				next_friday = temp_date + datetime.timedelta(7)
				if(next_friday.month != temp_date.month):
					dates.append(temp_date + datetime.timedelta(1))
	print dates
	return dates;
