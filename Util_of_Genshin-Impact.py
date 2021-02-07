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
	print('pip install pillow' + module_name)
	time.sleep(3)
	exit(1)

import time
import datetime
import os
import platform
import sys
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

def mosaic(src, ratio=0.1):
	small = cv2.resize(src, None, fx=ratio, fy=ratio, interpolation=cv2.INTER_NEAREST)
	return cv2.resize(small, src.shape[:2][::-1], interpolation=cv2.INTER_NEAREST)

def mosaic_area(src, x, y, width, height, ratio=0.1):
	dst = src.copy()
	dst[y:y + height, x:x + width] = mosaic(dst[y:y + height, x:x + width], ratio)
	return dst



currenttime = str(datetime.datetime.today())
currenttime = currenttime.replace(':','-').replace(' ','-')
currenttime = currenttime[:currenttime.find('.')]
currenttime = currenttime[2:]

saveToDir = os.getcwd()
if saveToDir[-1:] != '\\' and saveToDir[-1:] != '/':
	saveToDir += '/'

if str(platform.system()).lower() == 'windows':
	saveToDir = saveToDir.replace('/', '\\')

imagefname = ( saveToDir ) + ( 'ss' + '_' + currenttime + '.jpg' )

print('Dst' + ( '[' + '0' + ']' ) + ': ' + saveToDir)

# 引数チェック・引数があるか
# https://qiita.com/orange_u/items/3f0fb6044fd5ee2c3a37
args = sys.argv
if ( len(args) - 1 ) < 1:
	# 無いときはクリップボードからロード
	im = ImageGrab.grabclipboard()

	if isinstance(im, Image.Image):
		# 処理しやすいように一旦保存
		im.save(imagefname)

		# ファイルパスを表示
		print('saved: ' + imagefname)

		# ファイルパスをコピー
		pyperclip.copy('"' + imagefname + '"')

		# 引数として登録
		args.append(imagefname)

	else:
		print('no image in clipboard')

# 引数のファイルすべてロード
for i, item in enumerate(args):
	if i == 0: continue

	src = item
	print('Src' + ( '[' + str(i) + ']' ) + ': ' + src)

	if not os.path.isfile(item):
		print('Error: No such a file or directory: ' + item)
		time.sleep(3)
		exit(2)

	print('Dst' + ( '[' + str(i) + ']' ) + ': ' + imagefname)

	src = cv2.imread(src)
	if src is None:
		print('Error: Unable to load file: ' + item)
		time.sleep(3)
		exit(2)

	h, w, _ = src.shape

	if True:
		print('Original')
		print('   width:  ' + str(w) + 'px')
		print('   height: ' + str(h) + 'px')

	if w != 1920 or h != 1080 :
		print('Not support size')

	# 大きさ
	xe = 250
	ye = 30

	# 始点
	xs = w-xe
	ys = h-ye

	cv2.imwrite(imagefname, mosaic_area(src, xs, ys, xe, ye, ratio=0.2))
	print('')

time.sleep(1)
