"""
ファイル引数があるか
：ある→処理①
：ない→クリップボード読み取り

クリップボード読み取り
：画像→処理①
：その他→EXIT()

処理①
画像データか？
：はい→処理②
：いいえ→EXIT()

処理②
画像データ右下 xx pxをモザイク処理
"""

def err_ModuleNotFoundError(module_name):
	print('ModuleNotFoundError: Please run the below.')
	print('pip install ' + module_name)
	time.sleep(3)
	exit(1)

import time
import datetime
import os
import platform
import sys
import io
import numpy as np


try:
	import cv2
except ModuleNotFoundError:
	err_ModuleNotFoundError('opencv-python')

try:
	# クリップボード読み取り
	# https://code.tiblab.net/python/pil/clipboard_get_image
	from PIL import ImageGrab, Image
except ModuleNotFoundError:
	err_ModuleNotFoundError('pillow')

try:
	import pyperclip
except ModuleNotFoundError:
	err_ModuleNotFoundError('pyperclip')

try:
	import win32clipboard
except ModuleNotFoundError:
	err_ModuleNotFoundError('pywin32')






def mosaic(src, ratio=0.1):
	small = cv2.resize(src, None, fx=ratio, fy=ratio, interpolation=cv2.INTER_NEAREST)
	return cv2.resize(small, src.shape[:2][::-1], interpolation=cv2.INTER_NEAREST)

def mosaic_area(src, x, y, width, height, ratio=0.1):
	dst = src.copy()
	dst[y:y + height, x:x + width] = mosaic(dst[y:y + height, x:x + width], ratio)
	return dst

def getTimeString():
	now = str(datetime.datetime.today())
	now = now.replace(':','-').replace(' ','-')
	now = now[:now.find('.')+4]
	now = now.replace('.','-')
	now = now[2:]
	return now

def getFilenameString(saveToDir = os.getcwd()):
	return ( saveToDir ) + ( 'ss' + '_' + getTimeString() + '.png' )

def copy_img_to_clip_board(img_ndarray):
	"""
	ndarray型の画像を引数にとって、クリップボードにコピーする関数
	https://jangle.tokyo/2020/07/07/post-2241/
	https://water2litter.net/rum/post/python_win32clipboard_set/
	"""
	output = io.BytesIO()
	# img_ndarray = cv2.cvtColor(img_ndarray, cv2.COLOR_BGR2RGB)
	img_pil = Image.fromarray(np.uint8(img_ndarray))  # <class 'PIL.Image.Image'>に変換
	img_pil.save(output, 'BMP')
	img_bmp = output.getvalue()[14:]
	output.close()
	win32clipboard.OpenClipboard()
	win32clipboard.EmptyClipboard()
	win32clipboard.SetClipboardData(win32clipboard.CF_DIB, img_ndarray)
	win32clipboard.CloseClipboard()


# 保存先フォルダ
saveToDir = os.getcwd()

# 保存先フォルダ：引数チェック・引数があるか
# https://qiita.com/orange_u/items/3f0fb6044fd5ee2c3a37
args = sys.argv
#print(args)
try:
	if os.path.isdir(args[1]):
		saveToDir = args[1]
		del args[1]
	
except IndexError:
	pass

if saveToDir[-1:] != '\\' and saveToDir[-1:] != '/':
	saveToDir += '/'

if str(platform.system()).lower() == 'windows':
	saveToDir = saveToDir.replace('/', '\\')

print('Dst' + ( '[' + '0' + ']' ) + ': ' + saveToDir)

# 引数チェック・引数があるか
# https://qiita.com/orange_u/items/3f0fb6044fd5ee2c3a37
args = sys.argv
if ( len(args) - 1 ) < 1:
	# 無いときはクリップボードからロード
	im = ImageGrab.grabclipboard()

	if isinstance(im, Image.Image):
		# 保存先ファイル名
		imagefname = getFilenameString(saveToDir)

		# 処理しやすいように一旦保存
		im.save(imagefname, "PNG")

		# ファイルパスを表示
		print('saved: ' + imagefname)

		# ファイルパスをコピー
		pyperclip.copy('"' + imagefname + '"')

		# 引数として登録
		args.append(imagefname)

	else:
		print('Error: No image in clipboard')
		time.sleep(3)
		exit(4)

if (len(args)-1) < 1:
	print('Error: Unable the open directory.')
	time.sleep(3)
	exit(2)


# 引数のファイルすべてロード
for i, item in enumerate(args):
	if i == 0: continue
	if os.path.isdir(item):
		print('Src' + ( '[' + str(i) + ']' ) + ': ')


	src = item
	print('Src' + ( '[' + str(i) + ']' ) + ': ' + src)

	if not os.path.isfile(item):
		print('Error: No such a file or directory: ' + item)
		if os.path.isdir(item) and i==1: continue
		time.sleep(3)
		exit(4)

	imagefname = getFilenameString(saveToDir)
	print('Dst' + ( '[' + str(i) + ']' ) + ': ' + imagefname)

	# ファイルパスをコピー
	pyperclip.copy('"' + imagefname + '"')

	src = cv2.imread(src)
	if src is None:
		print('Error: Unable to load file: ' + item)
		time.sleep(3)
		exit(8)

	h, w, _ = src.shape

	if True:
		print('Original')
		print('\twidth:  ' + str(w) + 'px')
		print('\theight: ' + str(h) + 'px')

	if not((w == 1920 and h == 1080) or (w == 1280 and h == 720)) :
		print('Not support size')
		continue

	# 大きさ
	xe = 250
	ye = 30

	# 始点
	xs = w-xe
	ys = h-ye

	imagebdata = mosaic_area(src, xs, ys, xe, ye, ratio=0.2)
	cv2.imwrite(imagefname, imagebdata)

	print('')
	try:
		print(type(imagebdata))
		copy_img_to_clip_board(imagebdata)

	except:
		import traceback
		traceback.print_exc()
		sys.exit(1)

time.sleep(1)
