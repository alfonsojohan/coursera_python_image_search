import zipfile
from zipfile import ZipFile, is_zipfile

from PIL import Image, PngImagePlugin
import pytesseract
import cv2 as cv
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\admin\AppData\Local\Tesseract-OCR\tesseract.exe'

# loading the face detection classifier
face_cascade = cv.CascadeClassifier(
    'readonly/haarcascade_frontalface_default.xml')

# GLOBALS
source_images = []
filename = 'readonly/small_img.zip'

# get user input
to_find = input("Enter word do you want to find: ").strip() or "Christopher" 
print("Searching for '{}' in image files. Grab a coffee, this may take a while...".format(to_find))

# check we are actually using a zipfile
assert(is_zipfile(filename))

# open the zipfile and get the list of files
with ZipFile(filename) as zipimgs:
    # loop thru all zipfile elements and add to the dict
    for entry in zipimgs.infolist():
        # reset the dictionary object
        result_dict = {'file': None, 'img': None}

        # print(entry.filename)
        print("Reading image from {}...".format(entry.filename))
        result_dict['file'] = entry.filename
        with zipimgs.open(entry) as f:
            result_dict['img'] = (Image.open(f).convert('RGB'))
            source_images.append(result_dict)

# Find the letters
for f in source_images:
    print("Searching for '{}' in file {}...".format(to_find, f['file']))
    f['txt'] = pytesseract.image_to_string(f['img'])
    if to_find.lower() in f['txt'].lower():
        print("Results found in file {}".format(f['file']))

