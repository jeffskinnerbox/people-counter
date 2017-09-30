# USAGE
# python videostream_demo.py
# python videostream_demo.py --picamera

# import the necessary packages
from imutils.video import VideoStream
import datetime
import argparse
import imutils
import time
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--picamera",
                help="include if the Raspberry Pi Camera should be used",
                type=int, default=-1)
args = vars(ap.parse_args())

# initialize the video stream and allow the cammera sensor to warmup
vs = VideoStream(usePiCamera=args["picamera"] > 0).start()
print("Camera warming up ...")
time.sleep(1)

# loop over the frames from the video stream
while True:
    # grab the frame from the threaded video stream and resize it
    # to have a maximum width of 400 pixels
    frame = vs.read()
    frame = imutils.resize(frame, width=400)

    # draw the timestamp on the frame
    timestamp = datetime.datetime.now()
    ts = timestamp.strftime("%A, %B %d, %Y - %I:%M:%S%p")
    cv2.putText(frame, ts, (10, frame.shape[0] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

    # show the frame
    cv2.imshow("Frame", frame)

    # if the `q` or esc key was pressed, break from the loop
    key = cv2.waitKey(1)
    if chr(key & 255) == 'q' or key == 27:
        print("Camera stopped by user ...")
        break

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
