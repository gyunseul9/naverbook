import re
import urllib.request
import os
from datetime import datetime

class Tag:

	def mainpage(soup,keyword,ranking):

		wrap = soup.find('div',{'id':'wrap'})
		container = wrap.find('div',{'id':'container'})
		content = container.find('div',{'id':'content'})
		#print('content:',content)
		section_bestseller = content.find('div',{'class':'section_bestseller'})

		if keyword == 'bid':
			basic = section_bestseller.find('ol',{'class':'basic'})
			li = basic.find_all('li')
			type_best = li[int(ranking)-1].find('div',{'class':'thumb type_best'})
			value = type_best.find('a').attrs['href']
			value = Utilities.tokenize(str(value),'=')
			value = value[1]

		elif keyword == 'update':
			acount_term = section_bestseller.find('dl',{'class':'acount_term'})
			term = acount_term.find('dd',{'class':'term'})
			value = term.get_text().strip()

		elif keyword == 'array':
			basic = section_bestseller.find('ol',{'class':'basic'})
			li = basic.find_all('li')
			value = len(li)			

		elif keyword == 'link':
			basic = section_bestseller.find('ol',{'class':'basic'})
			li = basic.find_all('li')
			type_best = li[int(ranking)-1].find('div',{'class':'thumb type_best'})
			value = type_best.find('a').attrs['href']

		elif keyword == 'thumbnail':
			basic = section_bestseller.find('ol',{'class':'basic'})
			li = basic.find_all('li')
			type_best = li[int(ranking)-1].find('div',{'class':'thumb type_best'})
			value = type_best.find('img').attrs['src']
			value = Utilities.tokenize(str(value),'?')
			value = value[0]

		elif keyword == 'title':
			basic = section_bestseller.find('ol',{'class':'basic'})
			li = basic.find_all('li')
			dl = li[int(ranking)-1].find('dl')
			dt = dl.find('dt').get_text().strip()
			value = dt

		elif keyword == 'author':
			basic = section_bestseller.find('ol',{'class':'basic'})
			li = basic.find_all('li')
			dl = li[int(ranking)-1].find('dl')
			dd = dl.find_all('dd')
			date = Utilities.remove_all_tag(str(dd[0]))
			value = Utilities.tokenize(str(date),'|')
			value = value[0].strip()

		elif keyword == 'publisher':
			basic = section_bestseller.find('ol',{'class':'basic'})
			li = basic.find_all('li')
			dl = li[int(ranking)-1].find('dl')
			dd = dl.find_all('dd')
			date = Utilities.remove_all_tag(str(dd[0]))
			value = Utilities.tokenize(str(date),'|')
			value = value[1].strip()			

		elif keyword == 'date':
			basic = section_bestseller.find('ol',{'class':'basic'})
			li = basic.find_all('li')
			dl = li[int(ranking)-1].find('dl')
			dd = dl.find_all('dd')
			date = Utilities.remove_all_tag(str(dd[0]))
			value = Utilities.tokenize(str(date),'|')
			value = value[2].strip()

		elif keyword == 'summary':
			basic = section_bestseller.find('ol',{'class':'basic'})
			li = basic.find_all('li')
			dl = li[int(ranking)-1].find('dl')
			dd = dl.find_all('dd')
			value = Utilities.remove_certaion_tag(str(dd[2]))
			value = Utilities.remove_all_tag(str(value))
			value = Utilities.replace_keyword(str(value),'\'','`')
			value = Utilities.replace_keyword(str(value),'&lt;','[')
			value = Utilities.replace_keyword(str(value),'&gt;',']')

		return value

	def subpage(soup,keyword,ranking):

		wrap = soup.find('div',{'id':'wrap'})
		container = wrap.find('div',{'id':'container'})
		spot = container.find('div',{'class':'spot'})
		book_info = spot.find('div',{'class':'book_info'})
		book_info_inner = book_info.find('div',{'class':'book_info_inner'})

		if keyword == 'pagenisbn':
			for div in book_info_inner.find_all("div"):
				#print(div.get('class'))
				if div.get('class') is None:
					numbers = re.findall('\d+', div.text)
	
			value = numbers

		return value	

class Utilities:

	def remove_certaion_tag(string):
		string = re.sub('<span.*?>.*?</span>', '', str(string), 0, re.I|re.S)
		return string

	def remove_all_tag(string):
		string = re.sub('<[^<]+?>', '', string)
		return string

	def replace_keyword(string,old,new):
		string = string.replace(old, new)
		return string		

	def tokenize(string, token):
		arr = []
		arr = string.split(token)
		return arr	
