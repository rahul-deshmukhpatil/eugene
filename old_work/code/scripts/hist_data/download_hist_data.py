import urllib
import urllib2
import lxml.html as LH
from decimal import Decimal
import cx_Oracle
import requests 


from urllib2 import Request, urlopen, URLError

def text(elt):
    return elt.text_content().replace(u'\xa0', u' ')

def getUrl(url, args):
	hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
				'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
				'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
				'Accept-Encoding': 'none',
				'Accept-Language': 'en-US,en;q=0.8',
				'Connection': 'keep-alive'}

	try:
		req = requests.post(url, data=args, headers=hdr)
		print req
		return req 
	except URLError as e:
		if hasattr(e, 'reason'):
			print 'We failed to reach a server.'
			print 'Reason: ', e.reason
		elif hasattr(e, 'code'):
			print 'The server couldn\'t fulfill the request.'
			print 'Error code: ', e.code

		exit(-1)
	return


con = cx_Oracle.connect('eugene/rahul@127.0.0.1/XE')
print "Con version : %s " %(con.version)

cur = con.cursor()
cur.execute('select * from securities')
for result in cur:
	symbol = result[0];
	print symbol 
	url = 'https://www.nseindia.com/products/content/equities/equities/eq_security.htm'
	values = {'name': symbol}
	data = urllib.urlencode(values)
	page = getUrl(url, data)
	print page 
	break;
cur.close()
con.commit()

