# Source: https://pythonprogramming.net/mog-background-reduction-python-opencv-tutorial/

import numpy as np
import cv2

# ######################## 1st Pass

cap = cv2.VideoCapture('/home/pi/Videos/People-Walking-Shot-From-Above.mp4')
fgbg = cv2.createBackgroundSubtractorMOG2()

whilei True:
    ret, frame = cap.read()

    fgmask = fgbg.apply(frame)

    cv2.imshow('fgmask',frame)
    cv2.imshow('frame',fgmask)


    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break


cap.release()
cv2.destroyAllWindows()

# ######################## 2nd Pass

cap = cv2.VideoCapture('/home/pi/Videos/People-Walking-Shot-From-Above.mp4')

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


