#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from PIL import Image, ImageDraw, ImageFilter
import grapefruit as gp
import argparse
import math
import sys
#import pyperclip
try:
    #__import__('pyperclip')
	import pyperclip
except ImportError:
	clipboard_available =  False
else:
	clipboard_available =  True


debug=False
gui=False
ryb=False
rybmode=1 #grapefruit ryb processing is not obvious

def mode(ryb):
	if rybmode in (0,2):
		return 'rgb'
	return 'ryb' if ryb else 'rgb'

def ascolor(hexcolor):
	return gp.Color.NewFromHtml(hexcolor)

def rybrgb(color):
	color = list(color.hsv)
	color[0] = gp.Color.RybToRgb(color[0])
	color = gp.Color.NewFromHsv(*tuple(color))
	return color

def asout(color, ryb=False):
	if (ryb and mode in (1,2)):
		color = rybrgb(color)
	return color.html

def comp(hexcolor, ryb=False):
	return asout(ascolor(hexcolor).ComplementaryColor(mode=mode(ryb)), ryb)
    

def mono(hexcolor):
    return [ c.html for c in ascolor(hexcolor).MonochromeScheme()]

def analog(hexcolor, ryb=False): 
	return [ asout(c, ryb) for c in ascolor(hexcolor).AnalogousScheme(mode=mode(ryb))]

def triadic(hexcolor, ryb=False): 
    return [ asout(c, ryb) for c in ascolor(hexcolor).TriadicScheme(mode=mode(ryb))]

def tetradic(hexcolor, ryb=False): 
	return [ asout(c, ryb) for c in ascolor(hexcolor).TetradicScheme(mode=mode(ryb))]

def splitcomp(hexcolor, ryb=False): 
	return [comp(c, ryb) for c in analog(hexcolor, ryb)]

def info2(c):
	return str(info(c.html))

def info(hexcolor, ryb=False):
	c = gp.Color.NewFromHtml(hexcolor)
	# if (ryb):
	# 	c = list(c.hsv)
	# 	c[0] = gp.Color.RgbToRyb(c[0])
	# 	c = gp.Color.NewFromHsv(*tuple(c))		
	x = c.xyz[0] / (c.xyz[0]+c.xyz[1]+c.xyz[2])
	y = c.xyz[1]/ (c.xyz[0]+c.xyz[1]+c.xyz[2])
	n =  (x-0.3320)/(0.1858-y)
	temp = int(437*n**3 + 3601*n**2 + 6861*n + 5517)
	return hexcolor, 'rgb:' + str(c.rgb), 'hsv:'+ str(c.hsv), 'hsl:'+str(c.hsl), str(temp)+"K"

def colorin(c):
	if ("-" == c):
		if (not sys.stdin.isatty()):
			for line in sys.stdin:
				#print(line.strip())
				return gp.Color.NewFromHtml(line.strip())
		else:
			if clipboard_available:
				return colorin(pyperclip.paste())
			else:
				raise Exception ("Clipboard is not available!")
	return gp.Color.NewFromHtml(c)

parser = argparse.ArgumentParser(description='Color harmonics tool')
parser.add_argument('color', help='Hex color (eg #ffffff) or - to read clipboard', type=colorin, nargs='?', default='-')
parser.add_argument('mode', help='Harmonic to compute', default='info', choices=['comp', 'triadic', 'tetradic', 'mono', 'analog', 'splitcomp','info','gui'],nargs='?')
parser.add_argument('-y', '--ryb', help='Use RYB colorspace',action="store_true")
args = parser.parse_args()

if (args.ryb):
    if (debug):
        print ('>> RYB space')
        #_rgb_to_ryb(args.color.html)
    ryb=True

if (debug):
	print ('>> in=' + str(args.color.hsv))
	print ('>> ' + str(info(args.color.html, ryb)))
	print (">> clipboard avilable = {}".format(clipboard_available))

if (args.mode != 'gui'):
    res = locals()[args.mode](args.color.html, ryb)
    if (type(res) != str):
        res = "\n".join(res)
        #pyperclip.copy(res)
    print (res)
else:
    gui=True


def col_to_point(color,x,y,ryb,width,outline='black'):
    h=color.hsv[0]
    s=math.sqrt(color.hsv[1])
    if (ryb):
        h = gp.Color.RgbToRyb(h)
    x=math.sin(math.radians(h+90))*s*80 +x
    y=math.cos(math.radians(h+90))*s*80 +y
    draw.ellipse((x-width, y-width, x+width, y+width), fill = color.html, outline = outline)

if (gui): 
	width = 600
	height = 220
	radius = 80
	rgbx = 200
	rybx = 400
	recy = 55 #44
	recx = 80
	c = args.color
	y = 0

	im = Image.new('RGB', (width,220))
	pix = im.load()
	draw = ImageDraw.Draw(im)
	draw.rectangle((0, 0, width, height), fill=c.html)
	for s in range(1,radius,3):
		for h in range(0,360,(radius-s)/12+1):
			x=math.sin(math.radians(h+90.0))*s
			y=math.cos(math.radians(h+90.0))*s
			#rgb=colorsys.hsv_to_rgb(h/360.0,s/80.0,1.0)
			rgb = gp.Color.NewFromHsv(h,1.0*s/radius,1).rgb
			ryb = gp.Color.NewFromHsv(gp.Color.RybToRgb(h),1.0*s/radius,1).rgb
			for xp in range(-2,2):
				for yp in range(-2,2):
					pix[x+rgbx+xp,y+110+yp] = tuple([int(round(f*255.0)) for f in rgb])
					pix[x+rybx+xp,y+110+yp] = tuple([int(round(f*255.0)) for f in ryb])
                    
	
	
	col_to_point(c,rgbx,height/2,False,10)
	#draw.rectangle((0, y, recx, y + recy), fill=c.html)
	col_to_point(c,rybx,height/2,True,10)
	#draw.rectangle((width-recx, y, width, y + recy), fill=c.html)

	
	# Complementary
	#y += recy
	# RGB
	c2=gp.Color.NewFromHtml(comp(c.html,False))
	col_to_point(c2,rgbx,110,False,10)
	print ("rgb-comp " + c2.html)
	draw.rectangle((0, y, recx, y + recy), fill=c2.html)
	# RYB
	c2=gp.Color.NewFromHtml(comp(c.html,True))
	col_to_point(c2,rybx,110,True,10)
	print ("ryb-comp " + c2.html)
	draw.rectangle((width-recx, y, width, y + recy), fill=c2.html)

	# Triadic
	y += recy
	# RGB
	c2 = triadic(c.html,False)
	col_to_point(gp.Color.NewFromHtml(c2[0]),rgbx,110,False,5,mono(c2[0])[1])
	col_to_point(gp.Color.NewFromHtml(c2[1]),rgbx,110,False,5,mono(c2[1])[1])
	print ("rgb-triadic1 " + c2[0])
	print ("rgb-triadic2 " + c2[1])
	draw.rectangle((0, y, recx/3, y + recy), fill=c2[0])
	draw.rectangle((recx/3, y, recx-recx/3, y + recy), fill=c2[1])
	# RYB
	c2 = triadic(c.html,True)
	col_to_point(gp.Color.NewFromHtml(c2[0]),rybx,110,True,5,mono(c2[0])[1])
	col_to_point(gp.Color.NewFromHtml(c2[1]),rybx,110,True,5,mono(c2[1])[1])
	print ("ryb-triadic1 " + c2[0])
	print ("ryb-triadic2 " + c2[1])
	draw.rectangle((width-recx/3, y, width, y + recy), fill=c2[0])
	draw.rectangle((width-recx/3*2, y, width-recx/3, y + recy), fill=c2[1])

	# Tetradic
	# RGB
	c2 = tetradic(c.html,False)
	col_to_point(gp.Color.NewFromHtml(c2[0]),rgbx,110,False,6, mono(c2[0])[1])
	print ("rgb-tetradic " + c2[0])
	draw.rectangle((recx-recx/3, y, recx, y + recy), fill=c2[0])
	# RYB
	c2 = tetradic(c.html,True)
	col_to_point(gp.Color.NewFromHtml(c2[0]),rybx,110,True,6,mono(c2[0])[1])
	print ("ryb-tetradic " + c2[0])
	draw.rectangle((width-recx, y, width-recx/3*2, y + recy), fill=c2[0])

	# Analog
	y += recy
	# RGB
	c2 = analog(c.html,False)
	col_to_point(gp.Color.NewFromHtml(c2[0]),rgbx,110,False,4,mono(c2[0])[1])
	col_to_point(gp.Color.NewFromHtml(c2[1]),rgbx,110,False,4,mono(c2[1])[1])
	print ("rgb-analog1 " + c2[0])
	print ("rgb-analog2 " + c2[1])
	draw.rectangle((0, y, recx/2, y + recy), fill=c2[0])
	draw.rectangle((recx, y, recx-recx/2, y + recy), fill=c2[1])
	# RYB
	c2 = analog(c.html,True)
	col_to_point(gp.Color.NewFromHtml(c2[0]),rybx,110,True,4,mono(c2[0])[1])
	col_to_point(gp.Color.NewFromHtml(c2[1]),rybx,110,True,4,mono(c2[1])[1])
	print ("ryb-analog1 " + c2[0])
	print ("ryb-analog2 " + c2[1])
	draw.rectangle((width-recx/2, y, width, y + recy), fill=c2[0])
	draw.rectangle((width-recx, y, width-recx/2, y + recy), fill=c2[1])


	# Split complementary
	y += recy
	# RGB
	c2 = splitcomp(c.html,False)
	col_to_point(gp.Color.NewFromHtml(c2[0]),rgbx,110,False,6,mono(c2[0])[1])
	col_to_point(gp.Color.NewFromHtml(c2[1]),rgbx,110,False,6,mono(c2[1])[1])
	print ("rgb-split1 " + c2[0])
	print ("rgb-split2 " + c2[1])
	draw.rectangle((0, y, recx/2, y + recy), fill=c2[0])
	draw.rectangle((recx, y, recx-recx/2, y + recy), fill=c2[1])
	# RYB
	c2 = splitcomp(c.html,True)
	col_to_point(gp.Color.NewFromHtml(c2[0]),rybx,110,True,6,mono(c2[0])[1])
	col_to_point(gp.Color.NewFromHtml(c2[1]),rybx,110,True,6,mono(c2[1])[1])
	print ("ryb-split1 " + c2[0])
	print ("ryb-split2 " + c2[1])
	draw.rectangle((width-recx/2, y, width, y + recy), fill=c2[0])
	draw.rectangle((width-recx, y, width-recx/2, y + recy), fill=c2[1])

	im.filter(ImageFilter.SMOOTH_MORE)
	im.show()
	#end GUI
