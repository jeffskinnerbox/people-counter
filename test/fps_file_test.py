#!/usr/bin/python3
#
# Maintainer:   jeffskinnerbox@yahoo.com / www.jeffskinnerbox.me
# Version:      0.3.0
#
# USAGE
#    python fps_file_test.py  -  just report the measurements
#    python fps_file_test.py -d  -  also display the video in a window
#
# SOURCE
#    "Faster video file FPS with cv2.VideoCapture and OpenCV" blog by Adrian Rosebrock                   #noqa
#    https://www.pyimagesearch.com/2017/02/06/faster-video-file-fps-with-cv2-videocapture-and-opencv     #noqa
#
# PURPOSE
#    This script compare the runtime and frame rate of processing a file when
#    using Adrian Rosebrock's imutils process threading utilities.


# import the necessary packages
from __future__ import print_function
from imutils.video import FileVideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import cv2
import os

# update your defaults based on the box your running on
if os.uname()[1] == "desktop":
    path = "/home/jeff/Videos/balls-bouncing.mp4"
elif os.uname()[1] == "BlueRpi":
    path = "/home/pi/Videos/balls-bouncing.mp4"

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
                help="path to video file used as input",
                required=False,
                default=path)
ap.add_argument("-d", "--display",
                help="display the video as its processed",
                required=False,
                action='store_true',
                default=False)
args = vars(ap.parse_args())


# ################################## 1st Pass ##################################

# open a pointer to the video stream, allow things to intiailize,
# and start the FPS timer
print("1st Pass: Simple read of frames from video file")
print("Pause to make sure the video stream initializes")
stream = cv2.VideoCapture(args["video"])
time.sleep(2.0)
print("Starting test...")
fps = FPS().start()

# loop over frames from the video file stream
while True:
    # grab the frame from the threaded video file stream
    (grabbed, frame) = stream.read()

    # if the frame was not grabbed, then we have reached the end
    # of the stream
    if not grabbed:
        break

    # resize the frame and convert it to grayscale (while still
    # retaining 3 channels)
    frame = imutils.resize(frame, width=450)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = np.dstack([frame, frame, frame])

    # display a piece of text to the frame (so we can benchmark
    # fairly against the fast method)
    cv2.putText(frame, "Slow Method", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # show the frame and update the FPS counter
    cv2.imshow("Frame", frame)

    # check to see if the frame should be displayed to our screen
    if args["display"]:
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        if chr(key & 255) == 'q' or key == 27:
            print("Video file stopped by user ...")
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

# created a *threaded *video stream, allow the camera sensor to warmup,
# and start the FPS counter
print("\n2nd Pass: Using THREADED frames from video file")
print("Pause to make sure the video stream initializes")
fvs = FileVideoStream(args["video"]).start()
time.sleep(2.0)
print("Starting test...")
fps = FPS().start()

# loop over frames from the video file stream
while fvs.more():
    # grab the frame from the threaded video file stream, resize
    # it, and convert it to grayscale (while still retaining 3
    # channels)
    frame = fvs.read()
    frame = imutils.resize(frame, width=450)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = np.dstack([frame, frame, frame])

    # display the size of the queue on the frame
    cv2.putText(frame, "Queue Size: {}".format(fvs.Q.qsize()), (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # show the frame and update the FPS counter
    cv2.imshow("Frame", frame)

    # check to see if the frame should be displayed to our screen
    if args["display"] > 0:
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        if chr(key & 255) == 'q' or key == 27:
            print("Video file stopped by user ...")
            break

    # update the FPS counter
    fps.update()

# stop the timer and display FPS information
fps.stop()
print("\telasped time: {:.2f}".format(fps.elapsed()))
print("\tapprox. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()
fvs.stop()
