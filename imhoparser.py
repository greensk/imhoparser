#!/usr/bin/python
# * coding: utf8 *
from urllib import urlopen
from lxml import etree
import simplejson
import sys

if len(sys.argv) < 2:
	print 'USAGE: imhoparser.py username'
	quit()
	
def getAuthor(elementUrl):
	elementText = urlopen(elementUrl).read().decode('utf8')
	elementDoc = etree.HTML(elementText)
	
	authorName = elementDoc.xpath('//*[@class="m-person-block-item-name"]')
	
	if len(authorName) and authorName[0].text is not None:
		return authorName[0].text.strip()
	else:
		return None
	
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
	
		url = 'http://%s.imhonet.ru/content/%s/rates/%d' % (username, content, rate)
		while 1:
			
			text = urlopen(url).read().decode('utf8')
			doc = etree.HTML(text)
			
			for element in doc.xpath('//*[@class="m-rate-list-item"]'):
				
				item = {'content' : {}, 'rate' : rate}
				
				item['content']['link'] = element.xpath('.//a[@class="m-rate-item-content-header-link"]')[0].attrib['href']
				item['content']['title'] = element.xpath('.//a[@class="m-rate-item-content-header-link"]')[0].text.strip()
				
				if content == 'books':
					authors = getAuthor(item['content']['link'])
					if authors is not None:
						item['content']['authors'] = authors
					
				genre = element.xpath('.//*[@class="m-rate-item-content-genres"]')
				if len(genre) and genre[0].text is not None:
					item['content']['genre'] = map(unicode.strip, genre[0].text.split(','))
				
				origin = element.xpath('.//*[@class="m-rate-item-content-countries"]')
				if len(origin) and origin[0].text is not None:
					item['content']['origin'] = origin[0].text.strip()
				
				country = element.xpath('.//*[@class="country"]')
				if len(country) and country[0].text is not None:
					item['content']['country'] = country[0].text.strip()
					
				info = element.xpath('.//*[@class="m-rate-item-text"]')
				if len(info) and info[0].text is not None:
					item['info'] = info[0].text.strip()
				
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

