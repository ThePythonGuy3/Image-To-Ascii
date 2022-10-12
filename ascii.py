from math import *
import os
from PIL import Image
import pyperclip

colors = [(0, 0, 0), (255, 0, 0), (0, 255, 0), (255, 255, 0), (0, 0, 255), (255, 0, 255), (0, 255, 255), (255, 255, 255)]
light = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
multV = 0.8

def maxOut(color):
	o = []
	if max(color) == 0:
		return (0, 0, 0)

	for i in color:
		o.append(int((i / max(color)) * 255))

	return tuple(o)

def evaluateColor(col):
	r, g, b = col
	color_diffs = []
	n = 0
	for color in colors:
		cr, cg, cb = color

		color_diff = sqrt((r - cr)**2 + (g - cg)**2 + (b - cb)**2)

		color_diffs.append((color_diff, color, n))
		n += 1

	return min(color_diffs)[2]

def getAscii(col):
	v = col[0] + col[1] + col[2]

	v /= 3
	v /= 255
	v *= len(light)
	v = int(v)

	return light[len(light) - v - 1]

def full(im):
	o = ""

	pix = im.load()
	w, h = im.size

	for i in range(h):
		for j in range(w):
			try:
				r, g, b, a = pix[j, i]
			except:
				r, g, b = pix[j, i]
				a = 255

			ai = a / 255
			col = (r * ai, g * ai, b * ai)
			if ai == 0:
				tb = 0
			else:
				tb = evaluateColor(mult(col, multV))

			o += f"\033[3{tb}m{getAscii(col)}\033[0m"
		o += "\n"
	print(o)
	pyperclip.copy(o)

def getSurround(im, pix, w, h, cl, x, y):
	nn = 0
	v = 0
	isit = 0
	for i in range(-1, 2):
		for j in range(-1, 2):
			nx = x + j
			ny = y + i

			tv = 1 << nn

			nn += 1

			if (nx == x and ny == y) or nx < 0 or ny < 0 or nx >= w or ny >= h:
				if nx < 0 or ny < 0 or nx >= w or ny >= h:
					isit += 1

				continue

			try:
				r, g, b, a = pix[nx, ny]
			except:
				r, g, b = pix[nx, ny]
				a = 255

			ai = a / 255
			col = (r * ai, g * ai, b * ai)
			if ai == 0:
				tb = 0
			else:
				tb = evaluateColor(mult(col, multV))

			if cl == tb:
				v += tv

			if tb == 0 or tb != cl:
				isit += 1

	ch = "•"

	backslashTb = [1, 3, 257, 263, 293, 329, 384]
	if v in backslashTb:
		ch = "\\"

	forwardTb = [4, 6, 68, 71, 77, 192, 356]
	if v in forwardTb:
		ch = "/"

	vbarTb = [130, 131, 134, 138, 162, 194, 386]
	if v in vbarTb:
		ch = "║"

	hbarTb = [40, 41, 42, 44, 104, 168, 296]
	if v in hbarTb:
		ch = "="
	#else:
	#	ch = str(v).ljust(3)

	if cl == 0:
		ch = " "

	return ch, isit > 1

def clean(im):
	nim = im.copy()

	pix = im.load()
	w, h = im.size

	npix = nim.load()

	for i in range(h):
		for j in range(w):
			try:
				r, g, b, a = pix[j, i]
			except:
				r, g, b = pix[j, i]
				a = 255

			ai = a / 255
			col = (r * ai, g * ai, b * ai)
			if ai == 0:
				tb = 0
			else:
				tb = evaluateColor(mult(col, multV))

			v, isit = getSurround(im, pix, w, h, tb, j, i)

			if not isit:
				npix[j, i] = (0, 0, 0)

	return nim

def outline(im):
	o = ""

	nim = clean(im)
	pix = nim.load()
	w, h = nim.size

	for i in range(h):
		for j in range(w):
			try:
				r, g, b, a = pix[j, i]
			except:
				r, g, b = pix[j, i]
				a = 255

			ai = a / 255
			col = (r * ai, g * ai, b * ai)
			if ai == 0:
				tb = 0
			else:
				tb = evaluateColor(mult(col, multV))

			ch, ist = getSurround(im, pix, w, h, tb, j, i)
			o += f"\033[3{tb}m{ch}\033[0m"
		o += "\n"
	print(o)
	pyperclip.copy(o)

def mult(c, i):
	return tuple([int(j * i) for j in c])

os.system("color")

while 1:
	direct = input("Address: ")

	im = Image.open(direct)
	w, h = im.size
	img = im.resize((w * 2, h), Image.NEAREST)

	typ = int(input("Mode: "))
	multV = float(input("Contrast multiply (0.8-1 recommended): "))

	if typ == 1:
		full(img)
	elif typ == 2:
		nim = im.copy()
		npix = nim.load()

		nnim = im.copy()
		nnpix = nnim.load()

		nnnim = im.copy()
		nnnpix = nnnim.load()

		pix = im.load()
		w, h = im.size
		for i in range(h):
			for j in range(w):
				try:
					r, g, b, a = pix[j, i]
				except:
					r, g, b = pix[j, i]
					a = 255

				mx = maxOut((r, g, b))
				evC = colors[evaluateColor(mult(mx, multV))]

				npix[j, i] = mx
				nnpix[j, i] = evC
				nnnpix[j, i] = mult(evC, ((r + g + b) / 3) / 255)
		im.show()
		nim.show()
		nnim.show()
		nnnim.show()
	else:
		outline(img)

	print

