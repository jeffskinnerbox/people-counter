#!/usr/bin/python3
#
# Maintainer:   jeffskinnerbox@yahoo.com / www.jeffskinnerbox.me
# Version:      0.1.0
#
# USAGE
#   To run the /dev/video camera  -  python3 videostream_test_2.py -s usb
#   To run the Raspberry Pi camera  -  python3 videostream_test_2.py -s picamera
#   To run using a file  -  python3 videostream_test_2.py -s file
#
# SOURCE
#   Modification of "Unifying picamera and cv2.VideoCapture into a single class with OpenCV"
#   https://www.pyimagesearch.com/2016/01/04/unifying-picamera-and-cv2-videocapture-into-a-single-class-with-opencv/


# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
import datetime
import argparse
import imutils
import time
import cv2


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--source",
                help="include if the Raspberry Pi Camera should be used",
                required=True,
                default='usb')      # values are: usb, picamera, file
ap.add_argument("-f", "--file_input",
                help="instead of a camera, use a file as your input stream",
                required=False,
                default="/home/jeff/Videos/People-Walking-Shot-From-Above.mp4")
args = vars(ap.parse_args())

# initialize the video stream and allow the cammera sensor to warmup
if args["source"] == 'picamera':
    vs = VideoStream(usePiCamera=True).start()
    print("Camera warming up ...")
    time.sleep(2.0)
elif args["source"] == 'usb':
    vs = VideoStream(usePiCamera=False).start()
    print("Camera warming up ...")
    time.sleep(2.0)
elif args["source"] == 'file':
    vs = cv2.VideoCapture(args["file_input"])
else:
    print("Improper parameter set in -f option ... Stopping")
    exit

fps = FPS().start()

# loop over the frames from the video stream or file
while True:
    # grab the frame from the threaded video stream and resize it
    # to have a maximum width of 600 pixels
    if args["source"] == 'picamera' or args["source"] == 'usb':
        frame = vs.read()
    else:
        ret, frame = vs.read()
    if frame is None:
        print("Reached end of file or stream ...")
        fps.stop()
        break
    frame = imutils.resize(frame, width=600)

    # draw the timestamp on the frame
    timestamp = datetime.datetime.now()
    ts = timestamp.strftime("%A, %B %d, %Y - %I:%M:%S%p")
    cv2.putText(frame, ts, (10, frame.shape[0] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

    # show the frame in a pop-up window
    cv2.imshow("Frame", frame)

    # update the frame count
    fps.update()

    # if the `q` or esc key was pressed, break from the loop
    key = cv2.waitKey(1)
    if chr(key & 255) == 'q' or key == 27:
        print("Camera stopped by user ...")
        fps.stop()
        break

# stop the timer and display FPS information
print("\telasped time: {:.2f}".format(fps.elapsed()))
print("\tapprox. FPS: {:.2f}".format(fps.fps()))

# cleanup by closing the window and stop video streaming
cv2.destroyAllWindows()
if args["source"] == 'picamera' or args["source"] == 'usb':
    vs.stop()
