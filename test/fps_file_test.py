#!/usr/bin/python3
#
# Maintainer:   jeffskinnerbox@yahoo.com / www.jeffskinnerbox.me
# Version:      0.2.0
#
# USAGE
#    python fps_picamera_test.py  -  just report the mesurements
#    python fps_picamera_test.py -d  -  also display the video in a window
#
# SOURCE
#    "Increasing Raspberry Pi FPS with Python and OpenCV"
#    https://www.pyimagesearch.com/2015/12/28/increasing-raspberry-pi-fps-with-python-and-opencv/           #noqa


# import the necessary packages
from __future__ import print_function
from imutils.video.pivideostream import PiVideoStream
from imutils.video import FPS
from picamera.array import PiRGBArray
from picamera import PiCamera
import argparse
import imutils
import time
import cv2


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-n", "--num-frames",
                help="# of frames to loop over for FPS test",
                type=int, default=100)
ap.add_argument("-d", "--display",
                help="Whether or not frames should be displayed",
                action='store_true')
args = vars(ap.parse_args())

print("\nNOTE: I believe the PiVideoStream.stop() method is designed for")
print("continious operation and not for capture of defined number of frames.")
print("As a result, you get an error in PiCamera.capture_continuous.\n")

# ################################## 1st Pass ##################################

# initialize the camera and stream
camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(320, 240))
stream = camera.capture_continuous(rawCapture,
                                   format="bgr", use_video_port=True)

# allow the camera to warmup and start the FPS counter
print("1st Pass: Reading", args["num_frames"], "frames from pi camera.")
print("Pi Camera warming up ...")
time.sleep(2.0)
print("Starting test...")
fps = FPS().start()

# loop over some frames
for (i, f) in enumerate(stream):
    # grab the frame from the stream and resize it to have a maximum
    # width of 400 pixels
    frame = f.array
    frame = imutils.resize(frame, width=400)

    # check to see if the frame should be displayed to our screen
    if args["display"]:
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        if chr(key & 255) == 'q' or key == 27:
            print("Camera stopped by user ...")
            break

    # clear the stream in preparation for the next frame and update
    # the FPS counter
    rawCapture.truncate(0)
    fps.update()

    # check to see if the desired number of frames have been reached
    if i == args["num_frames"]:
        break

# stop the timer and display FPS information
fps.stop()
print("\telasped time: {:.2f}".format(fps.elapsed()))
print("\tapprox. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()
rawCapture.close()
camera.close()


# ########################## 2nd Pass With Threading ###########################

# created a *threaded *video stream, allow the camera sensor to warmup,
# and start the FPS counter
print("\n2nd Pass: Reading", args["num_frames"], "frames from pi camera.")
print("Using THREADED frames from Pi Camera...")
vs = PiVideoStream().start()
time.sleep(2.0)
print("Starting test...")
fps = FPS().start()

# loop over some frames...this time using the threaded stream
while fps._numFrames < args["num_frames"]:
    # grab the frame from the threaded video stream and resize it
    # to have a maximum width of 400 pixels
    frame = vs.read()
    frame = imutils.resize(frame, width=400)

    # check to see if the frame should be displayed to our screen
    if args["display"] > 0:
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
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
