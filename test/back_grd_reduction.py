#!/usr/bin/python3
#
# Maintainer:   jeffskinnerbox@yahoo.com / www.jeffskinnerbox.me
# Version:      0.3.0
#
# Source: https://pythonprogramming.net/mog-background-reduction-python-opencv-tutorial/

import numpy as np
import cv2
import os

# update your defaults based on the box your running on
if os.uname()[1] == "desktop":
    path = "/home/jeff/Videos/balls-bouncing.mp4"
elif os.uname()[1] == "BlueRpi":
    path = "/home/pi/Videos/balls-bouncing.mp4"

# ################################## 1st Pass ##################################

cap = cv2.VideoCapture(path)
fgbg = cv2.createBackgroundSubtractorMOG2()

while True:
    ret, frame = cap.read()

    fgmask = fgbg.apply(frame)

    cv2.imshow('fgmask',frame)
    cv2.imshow('frame',fgmask)


    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break


cap.release()
cv2.destroyAllWindows()

# ################################## 2nd Pass ##################################

cap = cv2.VideoCapture(path)

# Background subtraction
fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows=True)

while True:
    ret, frame = cap.read()

    fgmask = fgbg.apply(frame)

    cv2.imshow('fgmask',frame)
    cv2.imshow('frame',fgmask)


    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break


cap.release()
cv2.destroyAllWindows()


