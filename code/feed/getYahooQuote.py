import urllib2
import sys
import re
from bs4 import BeautifulSoup
import urllib
import json

url = 'https://finance.yahoo.com/quote/5PAISA.NS'
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3','Accept-Encoding': 'none','Accept-Language': 'en-US,en;q=0.8','Connection': 'keep-alive'}
req = urllib2.Request(url, headers=hdr)
response = urllib2.urlopen(req)
equity_page = response.read()
bs4obj = BeautifulSoup(equity_page, "html.parser")
script = bs4obj.find("script",text=re.compile("root.App.main")).text
data = json.loads(re.search("root.App.main\s+=\s+(\{.*\})", script).group(1))
stores = data["context"]["dispatcher"]["stores"]
print stores
print stores[u'QuoteSummaryStore'] [u'summaryDetail'] ['volume']['raw']
print stores[u'QuoteSummaryStore'] [u'price'] [u'regularMarketPrice']['raw']
#print stores[u'QuoteSummaryStore'] [u'financialData'] [u'currentPrice']['raw']
