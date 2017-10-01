#!/usr/bin/python3
#
# Maintainer:   jeffskinnerbox@yahoo.com / www.jeffskinnerbox.me
# Version:      0.1.0
#
# USAGE
#
# SOURCE
#   "Unifying picamera and cv2.VideoCapture into a single class with OpenCV"
#   https://www.pyimagesearch.com/2017/02/06/faster-video-file-fps-with-cv2-videocapture-and-opencv/



# import the necessary packages
from imutils.video import FileVideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", required=True,
                help="path to input video file")
args = vars(ap.parse_args())

# start the file video stream thread and allow the buffer to start to fill
print("Starting video file thread...")
fvs = FileVideoStream(args["video"]).start()
time.sleep(1.0)

# start the FPS timer
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

    # update the frame count
    fps.update()

    # if the `q` or esc key was pressed, break from the loop
    key = cv2.waitKey(1)
    if chr(key & 255) == 'q' or key == 27:
        fps.stop()
        print("File stopped by user ...")
        break

# stop the timer and display FPS information
fps.stop()
print("\telasped time: {:.2f}".format(fps.elapsed()))
print("\tapprox. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()
fvs.stop()
