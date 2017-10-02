#!/usr/bin/python3
#
# Maintainer:   jeffskinnerbox@yahoo.com / www.jeffskinnerbox.me
# Version:      0.2.0


import os
import cv2
import time
import numpy
import imutils
import vstream
import myperson
import argparse
import datetime
import tracemess                                  # for debugging
from tracemess import get_linenumber
from imutils.video import FPS


# default parameters when stating the algorithm
defaults = {
    "path": "/home/pi/Videos",                        # path to video storage
    "file_in": "People-Walking-Shot-From-Above.mp4",  # video to be processed
    "file_rec": "recording.mp4",                      # video before processing
    "file_recP": "recordingP.mp4",                    # video after processing
    "warmup_time": 1.5,                               # sec for camera warm up
    "device_no": 0,                                   # usb video device number
    "color_red": (255, 0, 0),
    "color_blue": (0, 0, 255),
    "color_green": (0, 255, 0),
    "color_white": (255, 255, 255)
}

# update your defaults based on the box your running on
if os.uname()[1] == "desktop":
    defaults["path"] = "/home/jeff/Videos"
elif os.uname()[1] == "BlueRpi":
    defaults["path"] = "/home/pi/Videos"

# initial conditions when stating the algorithm
initials = {
    "cnt_up": 0,
    "cnt_down": 0
}


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser(description='This is the MassMutual Raspberry Pi \
                             + OpenCV people counter')
ap.add_argument("-s", "--source",
                help="include if the Raspberry Pi Camera should be used",
                required=False,
                choices=['file', 'usbcamera', 'picamera'],
                default='file')
ap.add_argument("-d", "--video_device",
                help="device number for input video",
                required=False,
                default=defaults["device_no"])
ap.add_argument("-i", "--file_in",
                help="path to video file that will be processed",
                required=False,
                default=defaults["path"] + '/' + defaults["file_in"])
ap.add_argument("-o", "--file_recP",
                help="path to file where the processed video is stored",
                required=False,
                default=defaults["path"] + '/' + defaults["file_recP"])
ap.add_argument("-r", "--file_rec",
                help="path to file where the unprocessed camera \
                video will be recorded",
                required=False,
                default=defaults["path"] + '/' + defaults["file_rec"])
ap.add_argument("-p", "--picamera",
                help="include if the Raspberry Pi Camera should be used",
                action='store_true')
args = vars(ap.parse_args())

# create trace message object
trc = tracemess.TraceMess(args["file_in"])

# Set Input and Output Counters
cnt_up = initials["cnt_up"]
cnt_down = initials["cnt_down"]

#cap = cv2.VideoCapture(args["file_in"])
cap = vstream.VStream(args["source"], args["file_in"])

# wait while camera warms up and VStream initialize
time.sleep(defaults["warmup_time"])

# Check if camera or file has opened successfully
if cap.isopen() is False:
    trc.error("Error opening video stream or file")
    trc.stop()
    exit

# Get current width and height of frame
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
trc.info({"line_no": get_linenumber(),
          "frame": {"width": width, "height": height,
                    "fps": cap.get(cv2.CAP_PROP_FPS),
                    "count": cap.get(cv2.CAP_PROP_FRAME_COUNT)}})

# Define the codec and create VideoWriter object
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
fourcc = cv2.VideoWriter_fourcc(*'MP4V')
fourcc = cv2.VideoWriter_fourcc('M', 'P', '4', 'V')
fourcc = cv2.VideoWriter_fourcc(*'a\0\0\0')
video_recP = cv2.VideoWriter(args["file_recP"],
                               fourcc, 20.0, (int(width), int(height)))

# Define the codec and create VideoWriter object
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
fourcc = cv2.VideoWriter_fourcc(*'MP4V')
fourcc = cv2.VideoWriter_fourcc('M', 'P', '4', 'V')
fourcc = cv2.VideoWriter_fourcc(*'a\0\0\0')
video_rec = cv2.VideoWriter(args["file_rec"],
                               fourcc, 20.0, (int(width), int(height)))
# Video properties
# cap.set(3, 160) # Width
# cap.set(4, 120) # Height

# Prints the capture properties to console
# for i in range(19):
#    print(i, cap.get(i))

w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
#w = cap.get(3)              # width of the frame
#h = cap.get(4)              # height of the frame
frameArea = h*w             # area of the frame
areaTH = frameArea/250

# Input / output lines
line_up = int(2*(h/5))      # draw blue line 2/5 from the bottom
line_down = int(3*(h/5))    # draw red line 3/5 from the bottom

up_limit = int(1*(h/5))
down_limit = int(4*(h/5))

trc.info({"line_no": get_linenumber(), "area threshold": areaTH,
          "lines": {"red y axis": str(line_down), "blue y axis": str(line_up)}})

line_down_color = defaults["color_red"]               # red
line_up_color = defaults["color_blue"]                # blue
pt1 = [0, line_down]
pt2 = [w, line_down]
pts_L1 = numpy.array([pt1, pt2], numpy.int32)
pts_L1 = pts_L1.reshape((-1, 1, 2))
pt3 = [0, line_up]
pt4 = [w, line_up]
pts_L2 = numpy.array([pt3, pt4], numpy.int32)
pts_L2 = pts_L2.reshape((-1, 1, 2))

pt5 = [0, up_limit]
pt6 = [w, up_limit]
pts_L3 = numpy.array([pt5, pt6], numpy.int32)
pts_L3 = pts_L3.reshape((-1, 1, 2))
pt7 = [0, down_limit]
pt8 = [w, down_limit]
pts_L4 = numpy.array([pt7, pt8], numpy.int32)
pts_L4 = pts_L4.reshape((-1, 1, 2))

# Background subtraction
fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows=True)

# Structural elements for morphogic filters
kernelOp = numpy.ones((3, 3), numpy.uint8)
kernelOp2 = numpy.ones((5, 5), numpy.uint8)
kernelCl = numpy.ones((11, 11), numpy.uint8)

# Variables
font = cv2.FONT_HERSHEY_SIMPLEX
persons = []
max_p_age = 5
pid = 1

# start the FPS timer
fps = FPS().start()

trc.info({"line_no": get_linenumber(), "cap.more": cap.more()})

# loop over the frames from the video stream or file
while cap.more():
    # grab the frame from the threaded video file stream
    frame = cap.read()

    # write the frame to a file, as capture and without processing
    video_rec.write(frame)

    # grab the frame from the threaded video file stream, resize it,
    # and convert it to grayscale
    frame = imutils.resize(frame, width=450)
    #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    for i in persons:
        i.age_one()   # age every person one frame
    #########################
    #   PRE-PROCESSING      #
    #########################

    # Apply subtraction of background
    fgmask = fgbg.apply(frame)
    fgmask2 = fgbg.apply(frame)

    # Binary to remove shadows (gray color)
    try:
        ret, imBin = cv2.threshold(fgmask, 200, 255, cv2.THRESH_BINARY)
        ret, imBin2 = cv2.threshold(fgmask2, 200, 255, cv2.THRESH_BINARY)
        # Opening (erode-> dilate) to remove noise
        mask = cv2.morphologyEx(imBin, cv2.MORPH_OPEN, kernelOp)
        mask2 = cv2.morphologyEx(imBin2, cv2.MORPH_OPEN, kernelOp)
        # Closing (dilate -> erode) to join white regions
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernelCl)
        mask2 = cv2.morphologyEx(mask2, cv2.MORPH_CLOSE, kernelCl)
    except:
        trc.info({"line_no": get_linenumber(), "made it here": 4})
        trc.info({"line_no": get_linenumber(),
                  "total count": {"enter": cnt_up, "exit": cnt_down}})
        trc.stop()
        break
    #################
    #    CONTOURS   #
    #################

    # RETR_EXTERNAL returns only extreme outer flags. All child contours are left behind.                #noqa
    _, contours0, hierarchy = cv2.findContours(mask2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)        #noqa
    for cnt in contours0:
        area = cv2.contourArea(cnt)
        if area > areaTH:
            #################
            #   TRACKING    #
            #################

            # Missing add conditions for multipersons, outputs and screen inputs              #noqa

            M = cv2.moments(cnt)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            x, y, w, h = cv2.boundingRect(cnt)

            new = True
            if cy in range(up_limit, down_limit):
                for i in persons:
                    if abs(cx-i.getX()) <= w and abs(cy-i.getY()) <= h:
                        # the object is near one already detected before
                        new = False
                        i.updateCoords(cx, cy)   # update coordinates in the object and resets age     #noqa
                        if i.going_UP(line_down, line_up) is True:
                            cnt_up += 1
                            trc.info({"line_no": get_linenumber(), "object": {"id":i.getId(),"direction": "up", "time": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())}})            #noqa
                            trc.feature({"line_no": get_linenumber(), "total count": {"enter": cnt_up, "exit": cnt_down, "time": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())}})   #noqa
                        elif i.going_DOWN(line_down, line_up) is True:
                            cnt_down += 1
                            trc.info({"line_no": get_linenumber(), "object": {"id":i.getId(),"direction": "down", "time": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())}})          #noqa
                            trc.feature({"line_no": get_linenumber(), "total count": {"enter": cnt_up, "exit": cnt_down, "time": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())}})   #noqa
                        break
                    if i.getState() == '1':
                        if i.getDir() == 'down' and i.getY() > down_limit:
                            i.setDone()
                        elif i.getDir() == 'up' and i.getY() < up_limit:
                            i.setDone()
                    if i.timedOut():
                        # remove from the list persons
                        index = persons.index(i)
                        persons.pop(index)
                        del i     # free memory of i
                if new is True:
                    p = myperson.MyPerson(pid, cx, cy, max_p_age)
                    persons.append(p)
                    pid += 1

            #################
            #   DRAWINGS    #
            #################
            cv2.circle(frame, (cx, cy), 5, defaults["color_blue"], -1)
            img = cv2.rectangle(frame, (x, y), (x+w, y+h), defaults["color_green"], 2)
            # cv2.drawContours(frame, cnt, -1, (0, 255, 0), 3)

    # END for cnt in contours0

    #########################
    # DRAWING TRAJECTORIES  #
    #########################
    for i in persons:
        # if len(i.getTracks()) >= 2:
            # pts = numpy.array(i.getTracks(), numpy.int32)
            # pts = pts.reshape((-1, 1, 2))
            # frame = cv2.polylines(frame, [pts], False, i.getRGB())
        # if i.getId() == 9:
            # print(str(i.getX()), ', ', str(i.getY()))
        cv2.putText(frame, str(i.getId()), (i.getX(), i.getY()),
                    font, 0.3, i.getRGB(), 1, cv2.LINE_AA)

    #################
    #     IMAGES    #
    #################
    str_up = 'UP: ' + str(cnt_up)
    str_down = 'DOWN: ' + str(cnt_down)
    frame = cv2.polylines(frame, [pts_L1], False, line_down_color, thickness=2)
    frame = cv2.polylines(frame, [pts_L2], False, line_up_color, thickness=2)
    frame = cv2.polylines(frame, [pts_L3], False, defaults["color_white"], thickness=1)
    frame = cv2.polylines(frame, [pts_L4], False, defaults["color_white"], thickness=1)
    cv2.putText(frame, str_up, (10, 40), font, 0.5,
                defaults["color_white"], 2, cv2.LINE_AA)
    cv2.putText(frame, str_up, (10, 40), font, 0.5,
                defaults["color_blue"], 1, cv2.LINE_AA)
    cv2.putText(frame, str_down, (10, 90), font, 0.5,
                defaults["color_white"], 2, cv2.LINE_AA)
    cv2.putText(frame, str_down, (10, 90), font, 0.5,
                defaults["color_red"], 1, cv2.LINE_AA)

    # draw the time stamp on the frame
    timestamp = datetime.datetime.now()
    ts = timestamp.strftime("%A, %B %d, %Y - %I:%M:%S%p")
    cv2.putText(frame, ts, (10, frame.shape[0] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.35, defaults["color_blue"], 1)

    cv2.imshow('Frame', frame)
    # cv2.imshow('Mask', mask)

    # write the frame after it has been processed
    video_recP.write(frame)

    # update the frame count
    fps.update()

    # pre-set ESC or 'q' to exit
    k = cv2.waitKey(1) & 0xFF
    if k == 27 or k == ord('q'):
        break
# END while(cap.isOpened())

# stop the timer and display FPS information
fps.stop()
print("\telapsed time: {:.2f}".format(fps.elapsed()))
print("\tapprox. FPS: {:.2f}".format(fps.fps()))

# do the final cleanup before exiting
trc.stop()
#cap.release()
cap.stop()
video_rec.release()
video_recP.release()
cv2.destroyAllWindows()
