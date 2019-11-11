import os
import sys
import time

class Createvideo:

	def __init__(self):
		print('init')

	def make_video(self):

		now = time.localtime()

		name = str(now.tm_year)+str(now.tm_mon)+str(now.tm_mday)

		command = 'ffmpeg -f image2 -r 1/6 -i /mnt/sda1/refactoring/books/images/merge_%d.png -vcodec mpeg4 -y /mnt/sda1/refactoring/books/images/books_{}.mp4'.format(name)

		result = os.system(command)

	def make(self):

		try:
			self.make_video()							

		except Exception as e:
			with open('./createvideo.log','a') as file:
				file.write('{} You got an error: {}\n'.format(datetime.datetime.now().strtime('%Y-%m-%d %H:%M:%S'),str(e)))																								

def run():
	createvideo = Createvideo()
	createvideo.make()

if __name__ == "__main__":
	run()