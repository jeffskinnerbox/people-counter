#!/usr/bin/python3
#
# Maintainer:   jeffskinnerbox@yahoo.com / www.jeffskinnerbox.me
# Version:      0.1.0
#
# USAGE
#   Run using a file  -  python3 videostream_test_4.py -s file -f path-to-file
#   Run using a USB web camera  -  python3 videostream_test_4.py -s usbcamera
#   Run using a pi camera  -  python3 videostream_test_4.py -s picamera
#
# SOURCE
#   "Unifying picamera and cv2.VideoCapture into a single class with OpenCV"
#   https://www.pyimagesearch.com/2017/02/06/faster-video-file-fps-with-cv2-videocapture-and-opencv/


# import the necessary packages
from imutils.video import FileVideoStream
from imutils.video import VideoStream
from imutils.video import FPS
import datetime
import argparse
import imutils
import time
import cv2


class VStream:
    vsource = None

    def __init__(self, source='file', path=None, queueSize=128, src=0,
                 resolution=(640, 480), framerate=30):
        # initialize the video stream along with the boolean:w

        # used to indicate if the thread should be stopped or not
        self.vsource = source
        if self.vsource == 'file':
            self.stream = FileVideoStream(path, queueSize=queueSize).start()
        elif self.vsource == 'usbcamera':
            self.stream = VideoStream(src=src, usePiCamera=False,
                                      resolution=resolution,
                                      framerate=framerate).start()
        elif self.vsource == 'picamera':
            self.stream = VideoStream(src=src, usePiCamera=True,
                                      resolution=resolution,
                                      framerate=framerate).start()

    def start(self):
        # start a thread to read frames from the file video stream
        return self.stream.start()

    def update(self):
        # keep looping infinitely until the thread indicator variable is set,
        # then stop the thread
        return self.stream.update()

    def read(self):
        # return next frame in the queue
        return self.stream.read()

    def more(self):
        # return True if there are still frames in the queue
        if self.vsource == 'file':
            return self.stream.more()
        else:
            return True

    def stop(self):
        # indicate that the thread should be stopped
        self.stream.stop()

    def isopen(self):
        # check if the camera or file is already open
        if self.vsource == 'picamera':
            #return self.stream.stream._check_camera_open()
            return True
        else:
            return self.stream.stream.isOpened()

    def get(self, obj):
        # acess cv2.VideoCapture.get() within the FileVideoStream class
        if self.vsource == 'picamera':
            if obj == cv2.CAP_PROP_FRAME_WIDTH:      # Width of the frames in the video stream
                return 640
            elif obj == cv2.CAP_PROP_FRAME_HEIGHT:   # Height of the frames in the video stream
                return 480
            elif obj == cv2.CAP_PROP_FPS:            # Frame rate
                return 30
            elif obj == cv2.CAP_PROP_FRAME_COUNT:    # Number of frames in the video file
                return 1
        else:
            return self.stream.stream.get(obj)


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--source",
                help="include if the Raspberry Pi Camera should be used",
                required=False,
                choices=['file', 'usbcamera', 'picamera'],
                default='file')
ap.add_argument("-f", "--file_input",
                help="instead of a camera, use a file as your input stream",
                required=False,
                default="/home/pi/Videos/People-Walking-Shot-From-Above.mp4")
args = vars(ap.parse_args())

# initialize the video stream
vs = VStream(source=args["source"], path=args["file_input"])

# wait while camera warms up and things initialize
time.sleep(1.0)

# start the FPS timer
fps = FPS().start()

# loop over the frames from the video stream or file
while vs.more():
    # grab the frame from the threaded video stream and resize it
    # to have a maximum width of 600 pixels
    frame = vs.read()
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

# stop the FPS timer and display FPS information
fps.stop()
print("\telapsed time: {:.2f}".format(fps.elapsed()))
print("\tapprox. FPS: {:.2f}".format(fps.fps()))

# cleanup by closing the window and stop video streaming
vs.stop()
cv2.destroyAllWindows()
