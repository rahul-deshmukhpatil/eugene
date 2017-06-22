#!/bin/python
import urllib
import urllib2

from urllib2 import Request, urlopen, URLError

def text(elt):
    return elt.text_content().replace(u'\xa0', u' ')

def get_url(url):

	if not url:
		print('URL provided to get_url is empty !!!')
		exit(-1)

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
			print('We failed to reach a server.')
			print('Reason: ', e.reason)
		elif hasattr(e, 'code'):
			print('The server couldn\'t fulfill the request.')
			print('Error code: ', e.code)

		exit(-1)

	#print(response.read())
	return response.read()

