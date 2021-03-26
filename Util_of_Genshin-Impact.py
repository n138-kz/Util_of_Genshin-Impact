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
		print('   width:  ' + str(w) + 'px')
		print('   height: ' + str(h) + 'px')

	if w != 1920 or h != 1080 :
		print('Not support size')
	else:
		# 大きさ
		xe = 250
		ye = 30

		# 始点
		xs = w-xe
		ys = h-ye

		cv2.imwrite(imagefname, mosaic_area(src, xs, ys, xe, ye, ratio=0.2))

	print('')

time.sleep(1)
