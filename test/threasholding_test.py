#!/usr/bin/python3
#
# Maintainer:   jeffskinnerbox@yahoo.com / www.jeffskinnerbox.me
# Version:      0.3.0
#

# holding OpenCV Python Tutorial - https://pythonprogramming.net/thresholding-image-analysis-python-opencv-tutorial/

import cv2
import numpy as np

img = cv2.imread(bookpage.jpg)
retval, threshold = cv2.threshold(img, 12, 255, cv2.THRESH_BINARY)
cv2.imshow(original, img)
cv2.imshow(threshold, threshold)
cv2.waitKey(0)
cv2.destroyAllWindows()
