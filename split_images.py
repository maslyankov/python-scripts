# Script splits all the images in specified folder in two.
# Uses Pillow module

from PIL import Image
from pip._vendor.distlib.compat import raw_input
import os

path = raw_input('Input Path (leave empty for current dir): ') or './'

dirs = os.listdir( path )

def is_jpg(filename):
    try:
        i=Image.open(filename)
        return i.format =='JPEG'
    except IOError:
        print("Skipping " + filename + " - not JPEG")
        return False

def split_img():
    print("Starting...")
    for item in dirs:
        if os.path.isfile(path+item) & is_jpg(path+item):
            img = Image.open(path+item)


            width, height = img.size
            f, e = os.path.splitext(path + item)

            cropped = img.crop((0, 0, width - 0, height - 7760/2))
            cropped.save(f + '_cam1.jpg', 'JPEG', quality=100, exif=img.info['exif'])
            print("Outputting: " + f + '_cam1.jpg')

            cropped = img.crop((0, 7760/2, width - 0, height - 0))
            cropped.save(f + '_cam2.jpg', 'JPEG', quality=100, exif=img.info['exif'])
            print("Outputting: " + f + '_cam2.jpg')

split_img()
