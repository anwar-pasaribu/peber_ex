from PIL import Image, ImageFilter
import urllib.request, io

print("ALL IMAGES MUST BE PNG FORMAT")
ext = input("Get Image From Computer or Internet?(c or i)")
if ext == "c":
	path = input("Background Image Path: ")
	fpath = input("Image Path: ")
if ext == "i":
	url = input("Background URL: ")
	furl = input("Image URL: ")
	path = io.StringIO(urllib.request.urlopen(url).read())
	fpath = io.StringIO(urllib.request.urlopen(furl).read())

background = Image.open(path)
product = Image.open(fpath)
x, y = background.size
x2, y2 = product.size
xmid, ymid = x / 2 - (x2 / 2), y / 2 - (y2 / 2)
a = int(xmid)
b = int(ymid)
background.paste(product, (a, b), product)
background.show()
print(a, b)
