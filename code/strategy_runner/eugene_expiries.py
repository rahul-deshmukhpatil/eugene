import os 
import datetime  
import logging

logger = logging.getLogger(os.environ['logger'])

def get_nearest_expiry(underlying, date):
	#get the nearest thursday
	if(underlying == 'BANKNIFTY'):
		return date

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
