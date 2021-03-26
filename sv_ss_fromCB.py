import datetime
currenttime = str(datetime.datetime.today())
currenttime = currenttime.replace(':','-').replace(' ','-')
currenttime = currenttime[:currenttime.find('.')]
currenttime = currenttime[2:]

import os
imagefname = 'C:\\Users\\yneon\\Downloads\\' + 'screenshot_' + currenttime + '.jpg'

import platform
if str(platform.system()).lower() == 'windows':
	imagefname = imagefname.replace('/', '\\')

print(imagefname)

# https://code.tiblab.net/python/pil/clipboard_get_image
try:
	from PIL import ImageGrab, Image
except ModuleNotFoundError:
	print('ModuleNotFoundError: Please run the below.')
	print('pip install pillow')
	exit()

im = ImageGrab.grabclipboard()
if isinstance(im, Image.Image):
	im.save(imagefname)
	print('saved: ' + imagefname)

	try:
		import pyperclip
	except ModuleNotFoundError:
		print('ModuleNotFoundError: Please run the below.')
		print('pip install pyperclip')
		exit()

	pyperclip.copy('"' + imagefname + '"')

else:
	print('no image in clipboard')
