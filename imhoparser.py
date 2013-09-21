#!/usr/bin/python
# * coding: utf8 *
from urllib import urlopen
from lxml import etree
import re
import simplejson
import sys

if len(sys.argv) < 2:
	print 'USAGE: imhoparser.py username'
	quit()
username = sys.argv[1]
firstPart = True
print '{'
for content in ['books', 'films']:
	
	if firstPart:
		firstPart = False
	else:
		print ','
		
	print '"%s" : [' % content
	first = True
	for rate in range(1,11):
	
		url = 'http://%s.imhonet.ru/content/%s/rates/all/?rate=%d' % (username, content, rate)
		while 1:
			
			text = urlopen(url).read().decode('utf8')
			doc = etree.HTML(text)
			
			for element in doc.xpath('//*[@class="element-type clearfix"]'):
				
				item = {'content' : {}, 'rate' : rate}
				
				item['content']['link'] = element.xpath('.//*[@class="title"]/a')[0].attrib['href']
				item['content']['title'] = element.xpath('.//*[@class="title"]/a')[0].text.strip()
				
				authors = element.xpath('.//*[@class="authors"]')
				if len(authors) and authors[0].text is not None:
					item['content']['authors'] = authors[0].text.strip()
					
				genre = element.xpath('.//*[@class="styles"]')
				if len(genre) and genre[0].text is not None:
					item['content']['genre'] = genre[0].text.strip()
					
				country = element.xpath('.//*[@class="country"]')
				if len(country) and country[0].text is not None:
					item['content']['country'] = country[0].text.strip()
					
				info = element.xpath('.//*[@class="info list-rates-info"]')
				if len(info) and len(info[0]):
					item['info'] = map(lambda str: str.strip(), info[0].text.split('<br>'))
				
				if first:
					first = False
				else:
					print ','
					
				print simplejson.dumps(item)
			
			nxt = doc.xpath('//a[@class="rarr"]')
			if len(nxt) == 0:
				break
				
			url = nxt[0].attrib['href']
	print ']'
print '}'	
			
			
			
			
		
