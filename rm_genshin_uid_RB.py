#
# Author: Yuu Takanashi
# License: MIT
#
# How to use: Look the README.md
# Support: Python 3.6 for Windows10
#

debug = False

def err_ModuleNotFoundError(module_name):
	print('ModuleNotFoundError: Please run the below.')
	print('pip install ' + module_name)
	time.sleep(3)
	exit(1)

# 起動情報
# https://qiita.com/motoki1990/items/8275dbe02d5fd5fa6d2d#%E7%8F%BE%E5%9C%A8%E3%81%AE%E6%97%A5%E4%BB%98
import datetime
datetime_init=datetime.datetime.today()
print(str(datetime_init.strftime("%Y/%m/%d %H:%M:%S")))

# 設定値
dst_prefix = ''
dst_postfix = '_' + str(datetime_init.strftime("%Y%m%dT%H%M%S"))
dst_postfix = '_' + str(int(datetime_init.timestamp()))

# 引数チェック・引数があるか
# https://qiita.com/orange_u/items/3f0fb6044fd5ee2c3a37
import time
import sys

args = sys.argv
args_len = len(args) - 1
if args_len < 1:
	print('Error: Required image file.')
	time.sleep(2)
	exit(1)

# 引数チェック・ファイルがあるか
# https://qiita.com/tortuepin/items/4a0669d8f275e966229e
# https://programming-study.com/technology/python-foreach/
# https://note.nkmk.me/python-opencv-mosaic/
# https://note.nkmk.me/python-opencv-pillow-image-size/
import os
try:
	import cv2
except ModuleNotFoundError:
	err_ModuleNotFoundError('opencv-python')


def mosaic(src, ratio=0.1):
	small = cv2.resize(src, None, fx=ratio, fy=ratio, interpolation=cv2.INTER_NEAREST)
	return cv2.resize(small, src.shape[:2][::-1], interpolation=cv2.INTER_NEAREST)

def mosaic_area(src, x, y, width, height, ratio=0.1):
	dst = src.copy()
	dst[y:y + height, x:x + width] = mosaic(dst[y:y + height, x:x + width], ratio)
	return dst

for i, item in enumerate(args):
	if i == 0: continue
	
	src = item
	print('Src' + ( '[' + str(i) + ']' ) + ': ' + src)

	if not os.path.isfile(item): 
		print('Error: Unable to load file: '+item)
		time.sleep(2)
		exit(2)
	
	dst = os.path.dirname(os.path.splitext(item)[0]) + '\\' + str(dst_prefix) + os.path.basename(os.path.splitext(item)[0]) + str(dst_postfix) + os.path.splitext(item)[1]
	if dst[0:1] == '\\':
		dst = dst[1:]
	print('Dst' + ( '[' + str(i) + ']' ) + ': ' + dst)
	
	src = cv2.imread(src)
	h, w, _ = src.shape
	if debug:
		print('w=' + str(w) + ', h=' + str(h))
	
	# 始点
	x1=w-250
	y1=h-30

	# 大きさ
	x2=250
	y2=30
	if debug:
		print('x1=' + str(x1) + ', x2=' + str(x2))
		print('y1=' + str(y1) + ', y2=' + str(y2))
	

	cv2.imwrite(dst, mosaic_area(src, x1, y1, x2, y2, ratio=0.2))
	print('')

time.sleep(2)
