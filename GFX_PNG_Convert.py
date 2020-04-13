# GFX_PNG_Convert.py
# Rory 2020
# A somewhat naive converter between the GFX and PNG file formats

from PIL import Image
from sys import argv
from struct import unpack
from glob import glob
from os import path

# Convert a .GFX file to a .PNG file
def GFXtoPNG(file):
    name = path.splitext(file)[0]

    with open(file, "rb") as f:
        gfx_img = f.read()

    pal = gfx_img[:768]
    w = unpack('<H', gfx_img[772:774])[0]
    h = unpack('<H', gfx_img[774:776])[0]
    data = gfx_img[776:]
    png_img = Image.frombytes("P", (w, h), data)
    png_img.putpalette(pal)

    png_img.convert("RGB").save(name + ".png","PNG")

# Convert a .PNG file to a .GFX file
def PNGtoGFX(file):
    name = path.splitext(file)[0]

    png_img = Image.open(file).convert("RGB").convert("P", palette=Image.ADAPTIVE, colors=256)
    pal = png_img.palette.getdata()[1]
    width, height = png_img.size
    data = list(png_img.getdata())

    gfx_img = open(name + ".gfx", 'wb')
    gfx_img.write(pal)
    gfx_img.write(b'\x00\x00\x00\x00')
    gfx_img.write(width.to_bytes(2, byteorder='little'))
    gfx_img.write(height.to_bytes(2, byteorder='little'))
    for d in data:
        gfx_img.write(d.to_bytes(1, byteorder='big'))

# if we receive no file arguments, convert all files of one type in the folder
if len(argv) < 2:
    print("TIP: Convert individual files with python " + argv[0] + " img1.gfx img2.gfx")
    choice = input("Would you like to convert:\n(1) All GFX in folder to PNG\n(2) All PNG in folder to GFX\nEnter 1 or 2: ")
    if choice == '1':
        for file in glob("*.gfx"):
            GFXtoPNG(file)
    if choice == '2':
        for file in glob("*.png"):
            PNGtoGFX(file)
# if we're passed some files, convert them all
else:
    for file in argv[1:]:
        ext = path.splitext(file)[1][1:].strip().lower()
        if ext == 'gfx':
            GFXtoPNG(file)
        elif ext == 'png':
            PNGtoGFX(file)
