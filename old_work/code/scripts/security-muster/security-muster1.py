import urllib
import urllib2
import lxml.html as LH
from decimal import Decimal
import cx_Oracle


from urllib2 import Request, urlopen, URLError

def text(elt):
    return elt.text_content().replace(u'\xa0', u' ')

def getUrl(url):
	hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
				'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
				'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
				'Accept-Encoding': 'none',
				'Accept-Language': 'en-US,en;q=0.8',
				'Connection': 'keep-alive'}

	req = urllib2.Request(url, headers=hdr)
	try:
		response = urllib2.urlopen(req)
	except URLError as e:
		if hasattr(e, 'reason'):
			print 'We failed to reach a server.'
			print 'Reason: ', e.reason
		elif hasattr(e, 'code'):
			print 'The server couldn\'t fulfill the request.'
			print 'Error code: ', e.code

		exit(-1)

	page = response.read()
	return page


def parseGoogleData(data, key):
	key=key + '\n'
	found = [row for row in data if (row[0] == key)]    # 3

	value = ''
	if (len(found)):
		value = found[0][1]

	#print "Key[%s:%s] in row[%s]" %(key, value, found)
	value=value.replace('\n', '')
	value=value.replace('%', '')
	value=value.replace(',', '')
	value=value.replace(' ', '')

	if (value == '-'):
		return ''

	return value

def getNumber(number):
	if (number == '-' or number == ''):
		return ''

	d = {'M': 6, 'B': 9, 'T': 12, 'Q': 15}
	if number[-1] in d:
		num, magnitude = number[:-1], number[-1]
		return str(Decimal(num) * 10 ** d[magnitude])
	else:
		return str(Decimal(number))


con = cx_Oracle.connect('eugene/rahul@127.0.0.1/XE')
print "Con version : %s " %(con.version)

url = 'https://www.nseindia.com/archives/nsccl/mult/C_CATG_JAN2017.T01'
page = getUrl(url)

for line in page.splitlines():
	fields = [x.strip() for x in line.split(',')]
	# [20, RELIANCE, EQ, INE002A01018, 1, 0.02]
	symbol = fields[1]
	series = fields[2]
	isin = fields[3]

	if ( series != "EQ" or len(isin) != 12 ):
		continue

	#get Data from Google
	url='https://www.google.com/finance?q=NSE:' + symbol
	#print "Symbol[%s], isin[%s] : %s" %(symbol, isin, url)

	#@TODO: If required later use this
	googleFinPage = getUrl(url)

	root = LH.fromstring(googleFinPage) 

	for table in root.xpath('//table[@class="snap-data"]'):
		#header = [text(th) for th in table.xpath('//th')]        # 1
		data = [[text(td) for td in tr.xpath('td')]  
				for tr in table.xpath('//tr')]                   # 2
		#data = [row for row in data if len(row)==len(header)]    # 3 
		#data = pd.DataFrame(data, columns=header)                # 4

		mktCap = getNumber(parseGoogleData(data, 'Mkt cap'))
		shares = getNumber(parseGoogleData(data, 'Shares'))
		PE = getNumber(parseGoogleData(data, 'P/E'))
		divYeild = parseGoogleData(data, 'Div/yield')
		EPS = getNumber(parseGoogleData(data, 'EPS'))
		netProfitMargin = getNumber(parseGoogleData(data, 'Net profit margin'))
		operatingMargin = getNumber(parseGoogleData(data, 'Operating margin'))
		EBITDmargin = getNumber(parseGoogleData(data, 'EBITD margin'))
		ROAAmargin = getNumber(parseGoogleData(data, 'Return on average assets'))
		ROAEmargin = getNumber(parseGoogleData(data, 'Return on average equity'))
		print "row: %s" %(data)
		print "Symbol[%s], isin[%s], mktCap[%s], shares[%s], PE[%s], divYeild[%s], EPS[%s], netProfitMargin[%s], operatingMargin[%s], EBITDmargin[%s], ROAAmargin[%s], ROAEmargin[%s]" %(symbol, isin, mktCap, shares, PE, divYeild, EPS, netProfitMargin, operatingMargin, EBITDmargin, ROAAmargin, ROAEmargin)
		#print(data)

		rows = [(symbol, 'NSE', mktCap, shares, PE, divYeild, EPS, netProfitMargin, operatingMargin, EBITDmargin, ROAAmargin, ROAEmargin)
]
		
		cur = con.cursor()
		cur.bindarraysize = 1
		cur.setinputsizes(20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20)
		cur.executemany("insert into securities( symbol, exchange, mkt_cap, shares, PE, div_yeild, eps, net_profit_margin, operating_margin, ebit_margin, roaa_margin, roae_margin) values (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12)", rows)
		con.commit()
		
		break;
		
