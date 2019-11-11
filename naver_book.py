# -*- coding: utf-8 -*- 

import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import datetime
import sys
from module_book import Utilities,Tag
from config import Configuration
from db import DBConnection,Query
import codecs
from slacker import Slacker
from PIL import Image, ImageDraw, ImageFont
import urllib.request

class Naverbook:

	def __init__(self,ranking,platform):
		self.ranking = ranking
		self.platform = platform

	def set_params(self):
		self.ranking = sys.argv[1]
		self.platform = sys.argv[2]

	def validate(self):
		default	= {
			'ranking':'1',
			'platform':'local'
		}

		self.ranking = default.get('ranking')	if self.ranking == '' else self.ranking
		self.platform = default.get('platform')	if self.platform == '' else self.platform.lower()

	def send_slack(self,channel,text):

		attachments_dict = dict()
		attachments_dict['text'] = text
		attachments = [attachments_dict]

		token = 'TOKEN'
		slack = Slacker(token)
		#slack.chat.post_message(channel, message)
		slack.chat.post_message(channel=channel, text=None, attachments=attachments, as_user=True)

	def make_message(self,src,bid,update,ranking,link,thumbnail,title,author,publisher,pages,isbn,summary,date):
		text = '출처:{}\n 게시번호:{}\n 업데이트:{}\n 순위: {}\n 링크:{}\n 사진:{}\n 제목:{}\n 작가:{}\n 출판사:{}\n 페이지수:{}\n ISBN:{}\n 요약:{}\n 등록일:{}\n'.format(src,bid,update,ranking,link,thumbnail,title,author,publisher,pages,isbn,summary,date)
		self.send_slack('#books', text)		

	def download_image(self,ranking,thumbnail):

		i = 11 - int(ranking)

		tmp = []
		tmp = thumbnail.split('/')

		tmp2 = tmp[len(tmp)-1]
		exe = tmp2.split('.')

		now = time.localtime()

		if now.tm_mon < 10:
			month = '0'+str(now.tm_mon)
		if now.tm_mday < 10:
			day = '0'+str(now.tm_mday)

		folder ='/mnt/sda1/refactoring/books/images/'	

		name = str(i)+'_'+str(now.tm_year)+str(now.tm_mon)+str(now.tm_mday)+'.'+exe[1]

		savename = folder+name

		urllib.request.urlretrieve(thumbnail, savename)

		with Image.open(folder+name) as image:
			thumbnail_name = 'thumbnail_'+name
			image.thumbnail((260,180))
			image.save(folder+thumbnail_name, quality=40)

	def make_image(self,src,update,ranking,thumbnail,title,pages,isbn,summary):

		i = 11 - int(ranking)

		tmp = []
		tmp = thumbnail.split('/')

		tmp2 = tmp[len(tmp)-1]
		exe = tmp2.split('.')

		now = time.localtime()

		if now.tm_mon < 10:
			month = '0'+str(now.tm_mon)
		if now.tm_mday < 10:
			day = '0'+str(now.tm_mday)

		folder ='/mnt/sda1/refactoring/books/images/'	

		thumbnail_name = 'thumbnail_'+str(i)+'_'+str(now.tm_year)+str(now.tm_mon)+str(now.tm_mday)+'.'+exe[1]		

		name = str(now.tm_year)+str(now.tm_mon)+str(now.tm_mday)

		target = Image.open('/mnt/sda1/refactoring/books/background.png')

		filename = '/mnt/sda1/refactoring/books/images/complate_{}_{}.png'.format(str(i),name)

		fontname = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
		
		headline = '#앤비의 책장 #{}월{}일\n#베스트셀러순위'.format(now.tm_mon,now.tm_mday)

		line1 = summary[:45].strip()
		line2 = summary[45:90].strip()
		line3 = summary[90:135].strip()		
		line4 = summary[135:180].strip()
		line5 = summary[180:225].strip()		

		contents1 = '출처:{}\n업데이트:{}\n\n순위:{}위'.format(src,update,ranking)	

		contents2 = '도서명:{}\n페이지수:{}\nISBN:{}\n\n{}\n{}\n{}\n{}\n{}'.format(title,pages,isbn,line1,line2,line3,line4,line5)	
		
		draw = ImageDraw.Draw(target)

		_title = ImageFont.truetype(fontname, 22)
		draw.text((180,50), headline, font=_title, fill=(49,97,224))

		_contents1 = ImageFont.truetype(fontname, 14)
		draw.text((220,110), contents1, font=_contents1, fill=(153,0,102))

		_contents2 = ImageFont.truetype(fontname, 15)
		draw.text((10,200), contents2, font=_contents2, fill='black')		

		target.save(filename)	

	def merge_image(self,ranking,thumbnail):

		i = 11 - int(ranking)

		tmp = []
		tmp = thumbnail.split('/')

		tmp2 = tmp[len(tmp)-1]
		exe = tmp2.split('.')

		now = time.localtime()

		if now.tm_mon < 10:
			month = '0'+str(now.tm_mon)
		if now.tm_mday < 10:
			day = '0'+str(now.tm_mday)

		folder ='/mnt/sda1/refactoring/books/images/'	

		card_name = 'complate_'+str(i)+'_'+str(now.tm_year)+str(now.tm_mon)+str(now.tm_mday)+'.png'
		thumbnail_name = 'thumbnail_'+str(i)+'_'+str(now.tm_year)+str(now.tm_mon)+str(now.tm_mday)+'.'+exe[1]
		merge_name = 'merge_'+str(i)+'.png'
	
		card_image = Image.open(folder+card_name)
		thumbnail_image = Image.open(folder+thumbnail_name)
		width , height = thumbnail_image.size
		area = (0,0,width,height)
		card_image.paste(thumbnail_image, area)
	
		card_image.save(folder+merge_name)

	def delete_image(self,ranking,thumbnail):

		i = 11 - int(ranking)

		tmp = []
		tmp = thumbnail.split('/')

		tmp2 = tmp[len(tmp)-1]
		exe = tmp2.split('.')

		now = time.localtime()

		if now.tm_mon < 10:
			month = '0'+str(now.tm_mon)
		if now.tm_mday < 10:
			day = '0'+str(now.tm_mday)

		folder ='/mnt/sda1/refactoring/books/images/'	

		download_name = str(i)+'_'+str(now.tm_year)+str(now.tm_mon)+str(now.tm_mday)+'.'+exe[1]		
		thumbnail_name = 'thumbnail_'+str(i)+'_'+str(now.tm_year)+str(now.tm_mon)+str(now.tm_mday)+'.'+exe[1]		
		complate_name = 'complate_'+str(i)+'_'+str(now.tm_year)+str(now.tm_mon)+str(now.tm_mday)+'.png'

		os.remove(folder+download_name)
		os.remove(folder+thumbnail_name)
		os.remove(folder+complate_name)					

	def crawling(self):

		self.validate()

		try:
			
			configuration = Configuration.get_configuration(self.platform)
			_host = configuration['host']
			_user = configuration['user']
			_password = configuration['password']
			_database = configuration['database']
			_port = configuration['port']
			_charset = configuration['charset']

			conn = DBConnection(host=_host,
				user=_user,
				password=_password,
				database=_database,
				port=_port,
				charset=_charset)

			now = time.localtime()			
	
			main = 'https://book.naver.com/bestsell/bestseller_list.nhn'				

			options = webdriver.ChromeOptions()
			options.add_argument('headless')
			options.add_argument('window-size=1920x1080')
			options.add_argument('disable-gpu')
			options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
			options.add_argument('lang=ko_KR')
			options.add_argument('--log-level=3')
			
			driver = webdriver.Chrome('/mnt/sda1/refactoring/books/chromedriver', chrome_options=options)
			driver.implicitly_wait(3)
			driver.get('about:blank')
			driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5];},});")
			driver.get(main)

			html = driver.page_source
			soup = BeautifulSoup(html, 'html.parser')

			src = '네이버 책'

			update = Tag.mainpage(soup,'update',self.ranking)
			array = Tag.mainpage(soup,'array',self.ranking)
			link = Tag.mainpage(soup,'link',self.ranking)
			bid = Tag.mainpage(soup,'bid',self.ranking)
			thumbnail = Tag.mainpage(soup,'thumbnail',self.ranking)
			title = Tag.mainpage(soup,'title',self.ranking)
			author = Tag.mainpage(soup,'author',self.ranking)
			publisher = Tag.mainpage(soup,'publisher',self.ranking)
			date = Tag.mainpage(soup,'date',self.ranking)
			summary = Tag.mainpage(soup,'summary',self.ranking)

			driver = webdriver.Chrome('/mnt/sda1/refactoring/books/chromedriver', chrome_options=options)
			driver.implicitly_wait(3)
			driver.get('about:blank')
			driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5];},});")
			driver.get(link)

			html = driver.page_source
			soup = BeautifulSoup(html, 'html.parser')

			pagenisbn = Tag.subpage(soup,'pagenisbn',self.ranking)	

			'''
			print('출처: ',src)
			print('게시번호 :',bid)
			print('업데이트 : ',update)
			print('순위: ',self.ranking,'/',array)
			print('상세보기: ',link)
			print('책표지: ',thumbnail)
			print('책제목: ',title)
			print('저자: ',author)
			print('출판사: ',publisher)
			print('출판일: ',date)
			print('요약: ',summary)
			print('페이지수: ',pagenisbn[0])
			print('ISBN: ',pagenisbn[1])	
			END'''

			link = 'http://13.209.99.123/response_book?api=book&column=isbn&keyword='+pagenisbn[1]									

			cnt = conn.exec_select_books(bid,update)

			print('cnt:',cnt)

			if cnt:
				print('overlap seq: ',cnt)
			else:	
				print('does not overlap seq: ',cnt)	
				conn.exec_insert_books(src,bid,update,self.ranking,link,thumbnail,title,author,publisher,pagenisbn[0],pagenisbn[1],summary,date)
				self.make_message(src,bid,update,self.ranking,link,thumbnail,title,author,publisher,pagenisbn[0],pagenisbn[1],summary,date)
				
				if(thumbnail):
					self.download_image(self.ranking,thumbnail)
					self.make_image(src,update,self.ranking,thumbnail,title,pagenisbn[0],pagenisbn[1],summary)
					self.merge_image(self.ranking,thumbnail)
					self.delete_image(self.ranking,thumbnail)
		except Exception as e:
			with open('./naverbook.log','a') as file:
				file.write('{} You got an error: {}\n'.format(datetime.datetime.now().strtime('%Y-%m-%d %H:%M:%S'),str(e)))

def run():
	naverbook = Naverbook('','')
	naverbook.set_params()
	naverbook.crawling()

if __name__ == "__main__":
	run()
