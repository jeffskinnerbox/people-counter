#!/usr/bin/python3
#
# Maintainer:   jeffskinnerbox@yahoo.com / www.jeffskinnerbox.me
# Version:      0.1.0
#
# USAGE
#    python fps_webcamera_test.py  -  report the frames per second
#    python fps_webcamera_test.py -d  -  also display the video in a window
#
# SOURCE
#    "Increasing Raspberry Pi FPS with Python and OpenCV"
#    https://www.pyimagesearch.com/2015/12/28/increasing-raspberry-pi-fps-with-python-and-opencv/        #noqa


# import the necessary packages
from __future__ import print_function
from imutils.video import WebcamVideoStream
from imutils.video import FPS
import argparse
import imutils
import time
import cv2
import sys


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-n", "--num-frames",
                help="# of frames to loop over for FPS test",
                type=int, default=100)
ap.add_argument("-d", "--display",
                help="Whether or not frames should be displayed",
                action='store_true')
args = vars(ap.parse_args())

# ################################## 1st Pass ##################################

# grab a pointer to the video stream and initialize the FPS counter
print("1st Pass: Reading", args["num_frames"], "frames from web camera.")
print("Web Camera warming up ...")
stream = cv2.VideoCapture(0)
time.sleep(2.0)
fps = FPS().start()

# loop over some frames
while fps._numFrames < args["num_frames"]:
    # grab the frame from the stream and resize it to have a maximum
    # width of 400 pixels
    (grabbed, frame) = stream.read()
    if frame is None:
        print("USB Web Camera has no frame ... exiting")
        sys.exit()
    else:
        frame = imutils.resize(frame, width=400)

    # check to see if the frame should be displayed to our screen
    if args["display"]:
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1)
        if chr(key & 255) == 'q' or key == 27:
            print("Camera stopped by user ...")
            break

    # update the FPS counter
    fps.update()

# stop the timer and display FPS information
fps.stop()
print("\telasped time: {:.2f}".format(fps.elapsed()))
print("\tapprox. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
stream.release()
cv2.destroyAllWindows()


# ########################## 2nd Pass With Threading ###########################

# created a *threaded *video stream, allow the camera senor to warmup,
# and start the FPS counter
print("\n2nd Pass: Reading", args["num_frames"], "frames from web camera.")
print("Using THREADED frames from webcam...")
vs = WebcamVideoStream(src=0).start()
fps = FPS().start()

# loop over some frames...this time using the threaded stream
while fps._numFrames < args["num_frames"]:
    # grab the frame from the threaded video stream and resize it
    # to have a maximum width of 400 pixels
    frame = vs.read()
    if frame is None:
        print("USB Web Camera has no frame ... exiting")
        sys.exit()
    else:
        frame = imutils.resize(frame, width=400)

    # check to see if the frame should be displayed to our screen
    if args["display"]:
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1)
        if chr(key & 255) == 'q' or key == 27:
            print("Camera stopped by user ...")
            break

    # update the FPS counter
    fps.update()

# stop the timer and display FPS information
fps.stop()
print("\telasped time: {:.2f}".format(fps.elapsed()))
print("\tapprox. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
