#
# Maintainer:   jeffskinnerbox@yahoo.com / www.jeffskinnerbox.me
# Version:      0.4.1
#
# Source: "Faster video file FPS with cv2.VideoCapture and OpenCV" blog by Adrian Rosebrock
#         https://www.pyimagesearch.com/2017/02/06/faster-video-file-fps-with-cv2-videocapture-and-opencv
#         http://www.pyimagesearch.com/2016/01/04/unifying-picamera-and-cv2-videocapture-into-a-single-class-with-opencv/
#         http://www.pyimagesearch.com/2015/12/21/increasing-webcam-fps-with-python-and-opencv/
#         https://github.com/jrosebr1/imutils/tree/master/imutils/video

# https://julien.danjou.info/blog/2016/python-exceptions-guide
# http://www.pythonforbeginners.com/error-handling/exception-handling-in-python

"""
A VideoCapture object has several properties that you can access and sometimes change:

CAP_PROP_POS_MSEC        # Current position of the video file in milliseconds or video capture timestamp
CAP_PROP_POS_FRAMES      # 0-based index of the frame to be decoded/captured next
CAP_PROP_POS_AVI_RATIO   # Relative position of the video file: 0 - start of the film, 1 - end of the film
CAP_PROP_FRAME_WIDTH     # Width of the frames in the video stream
CAP_PROP_FRAME_HEIGHT    # Height of the frames in the video stream
CAP_PROP_FPS             # Frame rate
CAP_PROP_FOURCC          # 4-character code of codec
CAP_PROP_FRAME_COUNT     # Number of frames in the video file
CAP_PROP_FORMAT          # Format of the Mat objects returned by retrieve(
CAP_PROP_MODE            # Backend-specific value indicating the current capture mode
CAP_PROP_BRIGHTNESS      # Brightness of the image (only for cameras)
CAP_PROP_CONTRAST        # Contrast of the image (only for cameras)
CAP_PROP_SATURATION      # Saturation of the image (only for cameras)
CAP_PROP_HUE             # Hue of the image (only for cameras)
CAP_PROP_GAIN            # Gain of the image (only for cameras)
CAP_PROP_EXPOSURE        # Exposure (only for cameras)
CAP_PROP_CONVERT_RGB     # Boolean flags indicating whether images should be converted to RGB
CAP_PROP_WHITE_BALANCE   # Currently not supported
CAP_PROP_RECTIFICATION   # Rectification flag for stereo cameras (note: only supported by DC1394 v 2.x backend currently)

Picamera 1.13 Documentation (Release 1.13) - https://media.readthedocs.org/pdf/picamera/latest/picamera.pdf
API - picamera.camera Module - http://picamera.readthedocs.io/en/release-1.13/api_camera.html

"""

# import the necessary packages
import cv2
from imutils.video import FileVideoStream
from imutils.video import VideoStream

class VStream:
    vsource = None

    def __init__(self, source='file', path=None, qs=128, src=0,
                 resolution=(640, 480), fr=30):
        """
        Only the PiCamera will allow you to set its resolution at creation
        time.  In other cases (i.e. usb camera or file), the function
        VideoCapture.set() needs to be used post-creation to set resolution.
        But this will not work uniformly for all types of cameras.  As a
        result, the frame must be resized manually to your desired resolution.
        """
        self.vsource = source
        self.target_width = resolution[0]
        self.target_height = resolution[1]

        if self.vsource == 'file':
            self.stream = FileVideoStream(path, queueSize=qs).start()
        elif self.vsource == 'usbcamera':
            self.stream = VideoStream(src=src, usePiCamera=False).start()
        elif self.vsource == 'picamera':
            self.stream = VideoStream(usePiCamera=True, resolution=resolution,
                                      framerate=fr).start()

        if self.vsource == 'picamera':
            # read one frame to determine the resolution of the camera
            #frame = self.read()
            #self.native_width = frame.shape[0]
            #self.native_height = frame.shape[1]
            # this isn't right but can't figure out the picarmera
            self.native_width = resolution[0]
            self.native_height = resolution[1]
        else:
            self.native_width = self.get(cv2.CAP_PROP_FRAME_WIDTH)
            self.native_height = self.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def native_res(self):
        return (self.native_width, self.native_height)

    def target_res(self):
        return (self.target_width, self.target_height)

    def resize(self, frame, resolution):
        return cv2.resize(frame, resolution)

    def start(self):
        """
        This start a thread to read frames from the file or video stream
        """
        return self.stream.start()

    def update(self):
        """This will keep looping infinitely until the thread indicator
        variable is set, which then stops the thread."""
        return self.stream.update()

    def read(self):
        """This returns the next frame in the queue."""
        return self.stream.read()

    def more(self):
        """This returns True if there are still frames in the queue."""
        if self.vsource == 'file':
            return self.stream.more()
        else:
            return True

    def stop(self):
        """This request that the video stream be stopped."""
        self.stream.stop()

    def isopen(self):
        """Check if the camera or file is already open and
        retrun True if it is and False otherwise."""
        if self.vsource == 'picamera':
            #return self.stream.stream._check_camera_open()
            return True
        else:
            return self.stream.stream.isOpened()

    def version(self):
        """Return the version number of the camera being used.
        Only works for the Pi Camera."""
        from pkg_resources import require
        if self.vsource == 'picamera':
            return require('picamera')[0].version
        else:
            return None

    def get(self, obj):
        """Access cv2.VideoCapture.get() within the FileVideoStream class"""

        if self.vsource == 'picamera':
            if obj == cv2.CAP_PROP_FRAME_WIDTH:      # width of the frames
                return self.native_width
            elif obj == cv2.CAP_PROP_FRAME_HEIGHT:   # height of the frames
                return self.native_height
            else:
                print("Value of " + str(obj) +
                      " not supported in VStream.get() for PiCamera")
                return None
        else:
            return self.stream.stream.get(obj)

