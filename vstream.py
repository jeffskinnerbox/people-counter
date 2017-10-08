#
# Maintainer:   jeffskinnerbox@yahoo.com / www.jeffskinnerbox.me
# Version:      0.3.0
#
# Source: "Faster video file FPS with cv2.VideoCapture and OpenCV" blog by Adrian Rosebrock
#         https://www.pyimagesearch.com/2017/02/06/faster-video-file-fps-with-cv2-videocapture-and-opencv
#         http://www.pyimagesearch.com/2016/01/04/unifying-picamera-and-cv2-videocapture-into-a-single-class-with-opencv/
#         http://www.pyimagesearch.com/2015/12/21/increasing-webcam-fps-with-python-and-opencv/
#         https://github.com/jrosebr1/imutils/tree/master/imutils/video


# import the necessary packages
import cv2
from imutils.video import FileVideoStream
from imutils.video import VideoStream


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

"""
Picamera 1.13 Documentation (Release 1.13) - https://media.readthedocs.org/pdf/picamera/latest/picamera.pdf
API - picamera.camera Module - http://picamera.readthedocs.io/en/release-1.13/api_camera.html

        self.POS_MSEC = vidcap.get(CAP_PROP_POS_MSEC)             # Current position of the video file in milliseconds or video capture timestamp
        self.POS_FRAMES = vidcap.get(CAP_PROP_POS_FRAMES)         # 0-based index of the frame to be decoded/captured next
        self.POS_AVI_RATIO = vidcap.get(CAP_PROP_POS_AVI_RATIO)   # Relative position of the video file: 0 - start of the film, 1 - end of the film
        self.FRAME_WIDTH = vidcap.get(CAP_PROP_FRAME_WIDTH)       # Width of the frames in the video stream
        self.FRAME_HEIGHT = vidcap.get(CAP_PROP_FRAME_HEIGHT)     # Height of the frames in the video stream
        self.FPS = vidcap.get(CAP_PROP_FPS)                       # Frame rate
        self.FOURCC = vidcap.get(CAP_PROP_FOURCC)                 # 4-character code of codec
        self.FRAME_COUNT = vidcap.get(CAP_PROP_FRAME_COUNT)       # Number of frames in the video file
        self.FORMAT = vidcap.get(CAP_PROP_FORMAT)                 # Format of the Mat objects returned by retrieve()
        self.MODE = vidcap.get(CAP_PROP_MODE)                     # Backend-specific value indicating the current capture mode
        self.BRIGHTNESS = vidcap.get(CAP_PROP_BRIGHTNESS)         # Brightness of the image (only for cameras)
        self.CONTRAST = vidcap.get(CAP_PROP_CONTRAST)             # Contrast of the image (only for cameras)
        self.SATURATION = vidcap.get(CAP_PROP_SATURATION)         # Saturation of the image (only for cameras)
        self.HUE = vidcap.get(CAP_PROP_HUE)                       # Hue of the image (only for cameras)
        self.GAIN = vidcap.get(CAP_PROP_GAIN)                     # Gain of the image (only for cameras)
        self.EXPOSURE = vidcap.get(CAP_PROP_EXPOSURE)             # Exposure (only for cameras)
        self.CONVERT_RGB = vidcap.get(CAP_PROP_CONVERT_RGB)       # Boolean flags indicating whether images should be converted to RGB
        self.WHITE_BALANCE = vidcap.get(CAP_PROP_WHITE_BALANCE)   # Currently not supported
        self.RECTIFICATION = vidcap.get(CAP_PROP_RECTIFICATION)   # Rectification flag for stereo cameras (note: only supported by DC1394 v 2.x backend currently)

"""
