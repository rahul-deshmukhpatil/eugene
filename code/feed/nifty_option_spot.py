 '''  
 Created on Oct 26, 2013  
   
 @author: pokerface  
   
 This code gets the spot price and options data from NSE India(www.nseindia.com) website  
   
 '''  
   
 import urllib2  
 from BeautifulSoup import BeautifulSoup  
 import datetime  
 import pandas  
 import csv  
 import os  
 import re  
 import logging  
 logging.basicConfig(format='%(levelname)s %(asctime)s:%(message)s',level=logging.DEBUG)  
   
 get_text = lambda x: x.getText()   
   
 option_site = 'http://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?symbol=&lt;symbol&gt;&amp;date=&lt;expiry&gt;&amp;instrument=&lt;imnt_type&gt;'  
 future_site = 'http://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuoteFO.jsp?underlying=&lt;symbol&gt;&amp;instrument=&lt;imnt_type&gt;'  
   
 fut_imnt_type = {'stock':'FUTSTK','index':'FUTIDX'}  
 opt_imnt_type = {'stock':'OPTSTK','index':'OPTIDX'}  
   
 def convert_to_date(dt):  
   try:  
     return datetime.datetime.strptime(dt[:2] + dt[2:5].title() + dt[5:],"%d%b%Y")  
   except ValueError:  
     return None  
   
 def convert_to_float(num):  
   try:  
     return float(num.replace(',',''))  
   except ValueError:  
     return None  
   
 def get_soup(site):  
   """get the html source for a web site"""  
   try:  
     logging.debug("Getting data from:" + site)      
       
     hdr = {'User-Agent': 'Web-Scraping',  
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',  
     'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',  
     'Accept-Encoding': 'none',  
     'Accept-Language': 'en-US,en;q=0.8',  
     'Connection': 'keep-alive'}  
       
     req = urllib2.Request(site, headers = hdr)  
   
     page = urllib2.urlopen(req).read()      
     return BeautifulSoup(page)      
   except:  
     logging.debug("Check the site: " + str(site))  
     raise    
     
   
 def get_spot_price(symbol,isIndex = True):  
   """Get spot price of an index or stock"""  
   logging.debug("Getting spot price for index: " + str(symbol))  
   imnt_type = fut_imnt_type['index'] if isIndex else fut_imnt_type['stock']  
   soup = get_soup(future_site.replace("&lt;symbol&gt;", symbol).replace("&lt;imnt_type&gt;", imnt_type))  
   try:  
     return float(eval(soup.find("div", {"id": "responseDiv"}).getString().replace('null', 'None'))['data'][0]['lastPrice'].replace(",",""))      
   except:  
     logging.debug("Check the site: " + str(site))  
     raise    
     
   
 def get_expiries(symbol):  
   """Get option expiries"""  
   soup = get_soup(option_site.replace("&lt;symbol&gt;", symbol).replace("&lt;expiry&gt;", "-").replace("&lt;imnt_type&gt;", "-"))  
   expiries = []  
   for i in soup.findAll('select')[1].findChildren('option'):  
     exp = convert_to_date(i.getText())  
     if exp:  
       expiries.append(exp)  
     
   return expiries  
   
 def get_option_data(symbol, location, isIndex = True):  
   """get option data from NSE web site for a given symbol e.g. NIFTY(all expiries) and save it as a csv to a given location"""  
     
   expiries = get_expiries(symbol)  
         
   for expiry in expiries:  
     imnt_type = opt_imnt_type['index'] if isIndex else opt_imnt_type['stock']  
     soup = get_soup(option_site.replace("&lt;symbol&gt;", symbol).replace("&lt;expiry&gt;", expiry.strftime("%d%b%Y").upper()).replace("&lt;imnt_type&gt;",imnt_type))  
   
     spot_price = get_spot_price(symbol, isIndex)  
     trade_date = datetime.datetime.strptime(re.findall(r'\w{3}\s\d{2},\s\d{4}', soup.findAll('table')[0].findChildren('td')[1].findChildren('span')[1].getText())[0],'%b %d, %Y')  
     table = soup.findAll('table')[2]  
     rows = table.findAll('tr')  
     headers =[]   
     header_cells = rows[1].findAll('th')  
     for i in header_cells:  
       headers.append(str(i.get('title')).replace(' ','_'))  
     
     call_length = len(header_cells)/2 +1  
       
     tup = []    
     
     for row in rows[2:]:      
       opts = map(convert_to_float,map(get_text, row.findAll('td')))   
       call = opts[:call_length]  
       call += ['call', trade_date.strftime('%Y%m%d'), spot_price, expiry.strftime('%Y%m%d')]   
       logging.debug(call)  
       tup.append(tuple(call))  
         
       put = opts[-call_length:][::-1]      
       put += ['put', trade_date.strftime('%Y%m%d'), spot_price, expiry.strftime('%Y%m%d')]    
       logging.debug(put)    
       tup.append(tuple(put))    
       
     logging.debug('tuple:' + str(tup))  
     headers = headers[:call_length] + ['CallPut', 'trade_date', 'spot_price', 'expiry']      
     df = pandas.DataFrame(tup, columns = headers)    
           
     file = location + '/' + symbol + '_' + trade_date.strftime('%Y%m%d') + '_' + expiry.strftime('%Y%m%d') + '.csv'  
     df.to_csv(file)  
     logging.debug("Successfully saved:" + file)  
       
 if __name__ == '__main__':    
     
   print get_spot_price("ICICIBANK",isIndex = False)  
   print get_spot_price("NIFTY",isIndex = True)  
   get_option_data("ICICIBANK", 'D:/data', isIndex = False)  
   get_option_data("NIFTY", 'D:/data', isIndex = True)  
   
   
   
