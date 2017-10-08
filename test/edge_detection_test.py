#!/usr/bin/python3
#
# Maintainer:   jeffskinnerbox@yahoo.com / www.jeffskinnerbox.me
# Version:      0.3.0
#

# SOURCE
#    "Canny Edge Detection and Gradients OpenCV Python Tutorial" from the blog pythonprogramming.net
#    https://pythonprogramming.net/canny-edge-detection-gradients-python-opencv-tutorial/?completed=/morphological-transformation-python-opencv-tutorial/

import cv2
import numpy as np
import os

# update your defaults based on the box your running on
if os.uname()[1] == "desktop":
    path = "/home/jeff/Videos/balls-bouncing.mp4"
elif os.uname()[1] == "BlueRpi":
    path = "/home/pi/Videos/balls-bouncing.mp4"
cap = cv2.VideoCapture(1)

while(1):

    # Take each frame
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_red = np.array([30,150,50])
    upper_red = np.array([255,255,180])

    mask = cv2.inRange(hsv, lower_red, upper_red)
    res = cv2.bitwise_and(frame, frame, mask= mask)

    laplacian = cv2.Laplacian(frame, cv2.CV_64F)
    sobelx = cv2.Sobel(frame, cv2.CV_64F,1,0, ksize=5)
    sobely = cv2.Sobel(frame, cv2.CV_64F,0,1, ksize=5)

    cv2.imshow(Original, frame)
    cv2.imshow(Mask, mask)
    cv2.imshow(laplacian, laplacian)
    cv2.imshow(sobelx, sobelx)
    cv2.imshow(sobely, sobely)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()
