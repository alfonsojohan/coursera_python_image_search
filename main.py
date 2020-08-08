import zipfile
from zipfile import ZipFile, is_zipfile

from PIL import Image
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
    #f['txt'] = pytesseract.image_to_string(f['img'])
# if to_find.lower() in f['txt'].lower():
#     print("Results found in file {}".format(f['file']))
    print("Running face detection on file {}...".format(f['file']))
    #bgr_img = f['img'] # np.array(f['img'])  # [::-1].copy()
    bgr_img = cv.cvtColor(np.array(f['img']), cv.COLOR_RGB2BGR) 
    faces = face_cascade.detectMultiScale(bgr_img,
                                          scaleFactor=1.3,
                                          minSize=(50, 50),
                                          minNeighbors=5)
    print("Found {0} faces".format(len(faces)))

    for (x, y, w, h) in faces:
        cv.rectangle(bgr_img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        status = cv.imwrite('faces_detected-{}.jpg'.format(f['file'].split('.')[0]), bgr_img)
