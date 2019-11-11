# -*- coding: utf-8 -*- 
import sys
import requests
from requests_toolbelt import MultipartEncoder
import logging
import datetime
import time

class Postfacebook:

	def __init__(self):
		print('init')

	def upload_video(self,uri,pageid,token,description,title):

		log = logging.getLogger(__name__)

		video_file_name = uri.split("/")[-1]

		if video_file_name and video_file_name.count(".") == 0:
			log.debug("video_file_name has no ext {0}".format(video_file_name))
			video_file_name = "{0}.mp4".format(video_file_name)
			log.debug("video_file_name converted to {0}".format(video_file_name))

		path = "{0}/videos".format(pageid)

		fb_url = "https://graph-video.facebook.com/{0}?access_token={1}".format(path,token)

		log.debug("video_file = {0}".format(uri))
		log.debug("start upload to facebook")

		m = MultipartEncoder(
			fields={'description': description,
					'title': title,
					'source': (video_file_name, open(uri, 'rb'))}
			)

		r = requests.post(fb_url, headers={'Content-Type': m.content_type}, data=m)

		if r.status_code == 200:
 			j_res = r.json()
 			facebook_video_id = j_res.get('id')
 			log.debug("facebook_video_id = {0}".format(facebook_video_id))
		else:
			log.error("Facebook upload error: {0}".format(r.text))

		return facebook_video_id

	def execute(self):

		try:

			now = time.localtime()

			pageid = ''

			token = ''

			uri = '/mnt/sda1/refactoring/books/images/books_{}{}{}.mp4'.format(now.tm_year,now.tm_mon,now.tm_mday)
			
			title = '#앤비의 책장 #{}월{}일 #베스트셀러순위'.format(now.tm_mon,now.tm_mday)
			description = '#앤비의 책장 #{}월{}일 #베스트셀러순위'.format(now.tm_mon,now.tm_mday)

			result = self.upload_video(uri,pageid,token,description,title)

			print('result:',result)				

		except Exception as e:
			with open('./postfacebook.log','a') as file:
				file.write('{} You got an error: {}\n'.format(datetime.datetime.now().strtime('%Y-%m-%d %H:%M:%S'),str(e)))																								
def run():
	postfacebook = Postfacebook()
	postfacebook.execute()

if __name__ == "__main__":
	run()