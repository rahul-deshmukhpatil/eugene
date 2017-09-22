import datetime

ACCETABLE_EXCEPTION = 'EUGENE_ACCEPTABLE_EXCEPTION '

class NoSpotForDay():
	def __init__(date):
		self.date = date

	def log():
		return ACCETABLE_EXCEPTION + 'Could not find spot for date : ' + str(self.date)
