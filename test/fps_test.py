#!/usr/bin/python3
#
# Maintainer:   jeffskinnerbox@yahoo.com / www.jeffskinnerbox.me
# Version:      0.1.0
#
# USAGE
#    python picamera_fps_demo.py
#    python picamera_fps_demo.py -d  -  also display the video in a window
#
# SOURCE
#    "Increasing Raspberry Pi FPS with Python and OpenCV"
#    https://www.pyimagesearch.com/2015/12/28/increasing-raspberry-pi-fps-with-python-and-opencv/# USAGE


# import the necessary packages
from __future__ import print_function
from imutils.video import WebcamVideoStream
from imutils.video import FPS
import argparse
import imutils
import cv2
import sys
import os


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--source",
                help="include if the Raspberry Pi Camera should be used",
                required=True,
                default='usb')      # values are: usb, picamera, file
ap.add_argument("-n", "--num-frames",
                help="# of frames to loop over for FPS test",
                type=int, default=100)
ap.add_argument("-d", "--display",
                help="Whether or not frames should be displayed",
                action='store_true')
ap.add_argument("-f", "--file_input",
                help="instead of a camera, use a file as your input stream",
                required=False,
                default="/home/jeff/Videos/People-Walking-Shot-From-Above.mp4")
args = vars(ap.parse_args())


if args["source"] == 'picamera':
    from imutils.video.pivideostream import PiVideoStream
    from picamera.array import PiRGBArray
    from picamera import PiCamera


# ################################## 1st Pass ##################################

# initialize the camera and stream
if args["source"] == 'picamera':
    print("1st Pass: Reading", args["num_frames"], "frames from pi camera.")
    camera = PiCamera()
    camera.resolution = (320, 240)
    camera.framerate = 32
    rawCapture = PiRGBArray(camera, size=(320, 240))
    print("Pi Camera warming up ...")
#    stream = camera.capture_continuous(rawCapture, format="bgr",
#                                       use_video_port=True)
    # allow the camera to warmup and start the FPS counter
    fps = FPS().start()
elif args["source"] == 'usb':
    # grab a pointer to the video stream and initialize the FPS counter
    print("1st Pass: Reading", args["num_frames"], "frames from web camera.")
    print("Web Camera warming up ...")
    stream = cv2.VideoCapture(0)
    if stream == None:
        print("USB Web Camera has no frame ... exiting")
        sys.exit()
    fps = FPS().start()
elif args["source"] == 'file':
    print("1st Pass: Reading", args["num_frames"], "frames from file.")
    if not os.path.isfile(args["file_input"]):
        print("Files doesn't exist ... exiting")
        sys.exit()
    vs = cv2.VideoCapture(args["file_input"])
    fps = FPS().start()
else:
    print("Improper parameter set in -f option ... Stopping")
    exit

# loop over some frames
while fps._numFrames < args["num_frames"]:
    # grab the frame from the stream and resize it to have a maximum
    # width of 400 pixels
    if args["source"] == 'picamera':
        f = camera.capture_continuous(rawCapture, format="bgr", use_video_port=True)
        frame = f.array
        if frame == None:
            print("USB Web Camera has no frame ... exiting")
            sys.exit()
    if args["source"] == 'usb':
        (grabbed, frame) = stream.read()
        if frame == None:
            print("USB Web Camera has no frame ... exiting")
            sys.exit()
    else:
        ret, frame = vs.read()
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
    if args["source"] == 'picamera':
        rawCapture.truncate(0)
    fps.update()

# stop the timer and display FPS information
fps.stop()
print("\telasped time: {:.2f}".format(fps.elapsed()))
print("\tapprox. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()
if args["source"] == 'picamera':
    stream.close()
    rawCapture.close()
    camera.close()
elif args["source"] == 'usb':
    stream.release()
else:
    vs.release()


# ########################## 2nd Pass With Threading ###########################

# created a *threaded *video stream, allow the camera sensor to warmup,
# and start the FPS counter
if args["source"] == 'picamera':
    print("\n2nd Pass: Reading", args["num_frames"], "frames from pi camera.")
    print("Using THREADED frames from Pi Camera...")
    camera = PiCamera()
    camera.resolution = (320, 240)
    camera.framerate = 32
    rawCapture = PiRGBArray(camera, size=(320, 240))
    stream = camera.capture_continuous(rawCapture, format="bgr",
                                       use_video_port=True)
    # allow the camera to warmup and start the FPS counter
    print("Pi Camera warming up ...")
    vs = PiVideoStream().start()
    fps = FPS().start()
elif args["source"] == 'usb':
    # grab a pointer to the video stream and initialize the FPS counter
    print("\n2nd Pass: Reading", args["num_frames"], "frames from web camera.")
    print("Using THREADED frames from Web Camera...")
    print("Web Camera warming up ...")
    vs = WebcamVideoStream(src=0).start()
    fps = FPS().start()
elif args["source"] == 'file':
    print("\2nd Pass: Reading", args["num_frames"], "frames from file.")
    if not os.path.isfile(args["file_input"]):
        print("Files doesn't exist ... exiting")
        sys.exit()
    vs = cv2.VideoCapture(args["file_input"])
    fps = FPS().start()
else:
    print("Improper parameter set in -f option ... Stopping")
    exit

# loop over some frames...this time using the threaded stream
while fps._numFrames < args["num_frames"]:
    # grab the frame from the threaded video stream and resize it
    # to have a maximum width of 400 pixels
    if args["source"] == 'picamera':
        frame = vs.read()
    if args["source"] == 'usb':
        if frame == None:
            print("USB Web Camera has no frame ... exiting")
            sys.exit()
        frame = vs.read()
    else:
        ret, frame = vs.read()
    frame = imutils.resize(frame, width=400)

    # check to see if the frame should be displayed to our screen
    if args["display"]:
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
if args["source"] == 'picamera':
    stream.close()
    rawCapture.close()
    camera.close()
elif args["source"] == 'usb':
    vs.stop()
else:
    vs.release()
