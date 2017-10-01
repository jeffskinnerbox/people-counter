#
# Maintainer:   jeffskinnerbox@yahoo.com / www.jeffskinnerbox.me
# Version:      0.2.0

# import the necessary packages
from imutils.video import FileVideoStream
from imutils.video import VideoStream


class VStream:
    vsource = None

    def __init__(self, source, path=None, queueSize=128, src=0,
                 resolution=(320, 240), framerate=32):
        # initialize the video stream along with the boolean
        # used to indicate if the thread should be stopped or not
        self.vsource = source
        if self.vsource == 'file':
            self.stream = FileVideoStream(path, queueSize).start()
        elif self.vsource == 'usbcamera':
            self.stream = VideoStream(src=src, usePiCamera=False,
                                      resolution=resolution,
                                      framerate=framerate).start()
        elif self.vsource == 'picamera':
            self.stream = VideoStream(usePiCamera=True, resolution=resolution,
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

    def get(self, obj):
        # acess cv2.VideoCapture.get() within the FileVideoStream class
        if self.vsource == 'file':
            return self.stream.stream.get(obj)
        else:
            return self.stream.stream.get(obj)
