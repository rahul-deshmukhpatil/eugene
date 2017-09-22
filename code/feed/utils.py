import datetime

def get_date(dt):  
	try:  
		return datetime.datetime.strptime(dt[:2] + dt[2:5].title() + dt[5:],"%d%b%Y")  
	except ValueError:  
		return None  
   

