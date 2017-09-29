#!/usr/bin/python3
#
# Maintainer:   jeffskinnerbox@yahoo.com / www.jeffskinnerbox.me
# Version:      0.1.0

import cv2
import numpy
import myperson
import tracemess
import time
import argparse


source = {
    "path": "/home/jeff/Videos",
    "file": "People-Walking-Shot-From-Above.mp4",
    "device": "/dev/video0",
    "device_no": 0
}

sink = {
    "path": "/home/jeff/Videos",
    "file": "output.mp4",
    "device": ""
}

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--video_device", required=False,
                default=source["device_no"],
                help="device number for input video")
ap.add_argument("-f", "--video_file_in", required=False,
                default=source["path"] + '/' + source["file"],
                help="path to input video file")
ap.add_argument("-o", "--video_file_out", required=False,
                default=sink["path"] + '/' + sink["file"],
                help="path to output video file")
ap.add_argument("-p", "--picamera", required=False, type=int, default=-1,
                help="whether or not the Raspberry Pi camera should be used")
args = vars(ap.parse_args())


# Input and Output Counters
cnt_up = 0
cnt_down = 0

# Video Source
# cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture(args["video_file_in"])

# create trace message object
trc = tracemess.TraceMess(args["video_file_in"])

# Check if camera opened successfully
if (cap.isOpened() is False):
    trc.error("Error opening video stream or file")
    trc.stop()
    exit

# Get current width and height of frame
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
trc.info({"frame": {"width": width, "height": height,
                    "fps": cap.get(cv2.CAP_PROP_FPS),
                    "count": cap.get(cv2.CAP_PROP_FRAME_COUNT)}})

# Define the codec and create VideoWriter object
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
fourcc = cv2.VideoWriter_fourcc(*'MP4V')
fourcc = cv2.VideoWriter_fourcc('M', 'P', '4', 'V')
fourcc = cv2.VideoWriter_fourcc(*'a\0\0\0')
video_output = cv2.VideoWriter(args["video_file_out"],
                               fourcc, 20.0, (int(width), int(height)))

# Video properties
# cap.set(3, 160) # Width
# cap.set(4, 120) # Height

# Prints the capture properties to console
# for i in range(19):
#    print(i, cap.get(i))

w = cap.get(3)              # width of the frame
h = cap.get(4)              # height of the frame
frameArea = h*w             # area of the frame
areaTH = frameArea/250

# Input / output lines
line_up = int(2*(h/5))      # draw blue line 2/5 from the bottom
line_down = int(3*(h/5))    # draw red line 3/5 from the bottom

up_limit = int(1*(h/5))
down_limit = int(4*(h/5))

trc.info({"area threshold": areaTH, "lines": {"red y axis": str(line_down),
                                              "blue y axis": str(line_up)}})

line_down_color = (255, 0, 0)    # red
line_up_color = (0, 0, 255)      # blue
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

# Background subtractor
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

while(cap.isOpened()):
# for image in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):                 #noqa
    # Read an image from the video source
    ret, frame = cap.read()
#     frame = image.array

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
        trc.info({"total count": {"enter": cnt_up, "exit": cnt_down}})
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
                            trc.info({"object": {"id":i.getId(),"direction": "up", "time": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())}})            #noqa
                            trc.feature({"total count": {"enter": cnt_up, "exit": cnt_down, "time": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())}})   #noqa
                        elif i.going_DOWN(line_down, line_up) is True:
                            cnt_down += 1
                            trc.info({"object": {"id":i.getId(),"direction": "down", "time": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())}})          #noqa
                            trc.feature({"total count": {"enter": cnt_up, "exit": cnt_down, "time": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())}})   #noqa
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
            cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
            img = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
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
        cv2.putText(frame, str(i.getId()), (i.getX(), i.getY()), font, 0.3, i.getRGB(), 1, cv2.LINE_AA)  #noqa

    #################
    #     IMAGES    #
    #################
    str_up = 'UP: ' + str(cnt_up)
    str_down = 'DOWN: ' + str(cnt_down)
    frame = cv2.polylines(frame, [pts_L1], False, line_down_color, thickness=2)
    frame = cv2.polylines(frame, [pts_L2], False, line_up_color, thickness=2)
    frame = cv2.polylines(frame, [pts_L3], False, (255, 255, 255), thickness=1)
    frame = cv2.polylines(frame, [pts_L4], False, (255, 255, 255), thickness=1)
    cv2.putText(frame, str_up, (10, 40), font, 0.5, (255, 255, 255), 2, cv2.LINE_AA)  #noqa
    cv2.putText(frame, str_up, (10, 40), font, 0.5, (0, 0, 255), 1, cv2.LINE_AA)  #noqa
    cv2.putText(frame, str_down, (10, 90), font, 0.5, (255, 255, 255), 2, cv2.LINE_AA)  #noqa
    cv2.putText(frame, str_down, (10, 90), font, 0.5, (255, 0, 0), 1, cv2.LINE_AA)  #noqa

    cv2.imshow('Frame', frame)
    # cv2.imshow('Mask', mask)

    # write the flipped frame
    video_output.write(frame)

    # pre-set ESC or 'q' to exit
    k = cv2.waitKey(30) & 0xFF
    if k == 27 or k == ord('q'):
        break
# END while(cap.isOpened())

    #################
    #   CLEANING    #
    #################
trc.stop()
cap.release()
video_output.release()
cv2.destroyAllWindows()
