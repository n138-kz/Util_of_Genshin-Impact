# https://python.civic-apps.com/http-request-post-get/
try:
	import requests
except ModuleNotFoundError:
	print('ModuleNotFoundError: Please run the below.')
	print('pip install requests')
	exit()

response = requests.get('https://labs.n138.jp/GetRandStr/api/?chr=11&len=16')
if int(response.status_code) != 200:
	print('Error! HTTP status is ' + str(response.status_code))
	exit()

# https://docs.python.org/ja/3/library/json.html
import json
response = json.loads(response.text)
if response['result'] != True:
	print('Error! Parse error')
	exit()

response = response['detail']
print(response)



# pip install pillow
# https://code.tiblab.net/python/pil/clipboard_get_image
try:
	from PIL import ImageGrab, Image
except ModuleNotFoundError:
	print('ModuleNotFoundError: Please run the below.')
	print('pip install pillow')
	exit()

im = ImageGrab.grabclipboard()
if isinstance(im, Image.Image):
	im.save('screenshot_' + response + '.jpg')
	print('saved')
else:
	print('no image')
