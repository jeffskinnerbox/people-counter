#!/usr/bin/python3
#
# Maintainer:   jeffskinnerbox@yahoo.com / www.jeffskinnerbox.me
# Version:      0.4.1
#
# USAGE:
#     python3 app.py -s picamera  -  using pi camera and no trace messages

# Source: "People Counter" series of blog by Federico Mejia Barajas
#         http://www.femb.com.mx/people-counter/people-counter-9-counting/
#



import os
import sys
import cv2
import time
import numpy
import vstream
import myperson
import datetime
import tracemess                                      # for debugging
from imutils.video import FPS
from argparser import ArgParser
from tracemess import get_linenumber


# default paramsters when stating the video processing
defaults = {
    "version": "0.3.0",                               # algorithm version number
    "platform": os.uname(),                           # host your running on
    "trace_on": False,                                # turn on trace messaging
    "show": False,                                    # turn on video display
    "video_write_on": 'store_false',                  # turn on video storage
    "path": "/path/to/videos",                        # path to video storage
    "file_in": "People-Walking-Shot-From-Above.mp4",  # video to be processed
    "file_rec": "recording.mp4",                      # video before processing
    "file_recM": "recordingM.mp4",                    #
    "file_recP": "recordingP.mp4",                    # video after processing
    "warmup_time": 1.0,                               # sec for camera warm up
    "device_no": 0,                                   # usb video device number
    "resolution": [(640, 480)],                       # w,h resolution of frame
    "color_blue": (255, 0, 0),                        # opencv BGR color
    "color_green": (0, 255, 0),                       # opencv BGR color
    "color_red": (0, 0, 255),                         # opencv BGR color
    "color_yellow": (0, 255, 255),                    # opencv BGR color
    "color_white": (255, 255, 255),                   # opencv BGR color
    "color_black": (0, 0, 0),                         # opencv BGR color
    "font": cv2.FONT_HERSHEY_SIMPLEX,                 # font used on frame
    "max_p_age": 5
}

# initial conditions (people count) when stating the video processing
initials = {
    "cnt_up": 0,
    "cnt_down": 0
}


def calc_lines(capture, res):
    """ The frame will be divided into 5 horizontal zones of equal size.
    These zones, and how objects a managed within them, will be critical
    to the accurate accounting for the entry and exit of people.
    To make these zones visible to the user, boundary lines draw on the frame.
    """
    width = res[0]
    height = res[1]

    frameArea = height * width       # area of the frame
    areaTH = frameArea/250

    # Input / output lines
    line_up = int(2*(height/5))      # draw blue line 2/5 from the bottom
    line_down = int(3*(height/5))    # draw red line 3/5 from the bottom

    up_limit = int(1*(height/5))
    down_limit = int(4*(height/5))

    # red line coordinates calculations
    pt1 = [0, line_down]
    pt2 = [width, line_down]
    pts_L1 = numpy.array([pt1, pt2], numpy.int32)
    pts_L1 = pts_L1.reshape((-1, 1, 2))

    # blue line coordinates calculations
    pt3 = [0, line_up]
    pt4 = [width, line_up]
    pts_L2 = numpy.array([pt3, pt4], numpy.int32)
    pts_L2 = pts_L2.reshape((-1, 1, 2))

    # white line coordinates calculations
    pt5 = [0, up_limit]
    pt6 = [width, up_limit]
    pts_L3 = numpy.array([pt5, pt6], numpy.int32)
    pts_L3 = pts_L3.reshape((-1, 1, 2))

    # black line coordinates calculations
    pt7 = [0, down_limit]
    pt8 = [width, down_limit]
    pts_L4 = numpy.array([pt7, pt8], numpy.int32)
    pts_L4 = pts_L4.reshape((-1, 1, 2))

    trc.info({"width": width, "height": height})
    trc.info({"frameArea": frameArea, "areaTH": areaTH})
    trc.info({"line_up": line_up, "line_down": line_down})
    trc.info({"up_limit": up_limit, "down_limit": down_limit})
    trc.info({"Red Line": numpy.array_str(pts_L1)})
    trc.info({"Blue Line": numpy.array_str(pts_L2)})
    trc.info({"Yellow Line": numpy.array_str(pts_L3)})
    trc.info({"Black Line": numpy.array_str(pts_L4)})

    return line_up, line_down, up_limit, down_limit, areaTH,\
        pts_L1, pts_L2, pts_L3, pts_L4


def PeopleCounter(cap, resolution, cnt_up=0, cnt_down=0):                         # noqa: C901

    # calculate the placement of the counting lines
    line_up, line_down, up_limit, down_limit, areaTH,\
        pts_L1, pts_L2, pts_L3, pts_L4 = calc_lines(cap, args["resolution"][0])

    # Background subtraction
    fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows=True)

    # Structural elements for morphogic filters
    kernelOp = numpy.ones((3, 3), numpy.uint8)
    kernelOp2 = numpy.ones((5, 5), numpy.uint8)
    kernelCl = numpy.ones((11, 11), numpy.uint8)

    # Variables
    """
    font = cv2.FONT_HERSHEY_SIMPLEX
    max_p_age = 5
    """
    persons = []
    pid = 1

    # start the FPS timer
    fps = FPS().start()

    # loop over the frames from the video stream or file
    while cap.more():
        #trc.time_start(mess={"line#": get_linenumber()})

        # send a heartbeat when it's time
        trc.heartbeat({"text": "Still alive!!", "time":
                       time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())})

        # grab the frame from the threaded video file stream
        frame = cap.read()

        # resize the frame to your target resolution since
        # can't guarantee your camera is set for your target
        frame = cap.resize(frame, resolution)

        """
        # NOTE: CAN'T DO THIS AFTER CALCULATING LINES
        # grab the frame from the threaded video file stream, resize it
        frame = imutils.resize(frame, width=450)

        # convert frame it to grayscale
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        """

        # write the frame to a file, as capture and without processing
        if args["video_write_on"] is True:
            video_rec.write(frame)

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
            trc.info({"line#": get_linenumber(),
                      "EXCEPTION": {"enter": cnt_up, "exit": cnt_down}})
            break
        #################
        #    CONTOURS   #
        #################

        # RETR_EXTERNAL returns only extreme outer flags. All child contours are left behind.     #noqa: C901
        _, contours0, hierarchy = cv2.findContours(mask2, cv2.RETR_EXTERNAL,
                                                   cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours0:
            area = cv2.contourArea(cnt)
            if area > areaTH:
                #################
                #   TRACKING    #
                #################

                # Missing add conditions for multipersons, outputs and screen inputs              #noqa: C901

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
                            # update coordinates in the object and resets age
                            i.updateCoords(cx, cy)
                            if i.going_UP(line_down, line_up) is True:
                                cnt_up += 1
                                trc.feature({"line#": get_linenumber(),
                                    "object": {"id": i.getId(),
                                    "direction": "up",
                                    "time": time.strftime("%Y-%m-%d %H:%M:%S",
                                    time.gmtime())}})
                            elif i.going_DOWN(line_down, line_up) is True:
                                cnt_down += 1
                                trc.feature({"line#": get_linenumber(),
                                        "object": {"id": i.getId(),
                                        "direction": "down",
                                        "time": time.strftime("%Y-%m-%d %H:%M:%S",
                                        time.gmtime())}})
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
                        p = myperson.MyPerson(pid, cx, cy, defaults["max_p_age"])
                        persons.append(p)
                        pid += 1

                #################
                #   DRAWINGS    #
                #################
                cv2.circle(frame, (cx, cy), 5, defaults["color_green"], -1)
                img = cv2.rectangle(frame, (x, y), (x+w, y+h),
                                    defaults["color_green"], 2)
                #cv2.drawContours(frame, cnt, -1, defaults["color_black"], 3)

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
                        defaults["font"], 0.3, i.getRGB(), 1, cv2.LINE_AA)

        #################
        #     IMAGES    #
        #################
        str_up = 'UP: ' + str(cnt_up)
        str_down = 'DOWN: ' + str(cnt_down)
        frame = cv2.polylines(frame, [pts_L1], False,
                              defaults["color_red"], thickness=2)
        frame = cv2.polylines(frame, [pts_L2], False,
                              defaults["color_blue"], thickness=2)
        frame = cv2.polylines(frame, [pts_L3], False,
                              defaults["color_white"], thickness=1)
        frame = cv2.polylines(frame, [pts_L4], False,
                              defaults["color_yellow"], thickness=1)
        cv2.putText(frame, str_up, (10, 40), defaults["font"], 0.5,
                    defaults["color_white"], 2, cv2.LINE_AA)
        cv2.putText(frame, str_up, (10, 40), defaults["font"], 0.5,
                    defaults["color_blue"], 1, cv2.LINE_AA)
        cv2.putText(frame, str_down, (10, 90), defaults["font"], 0.5,
                    defaults["color_white"], 2, cv2.LINE_AA)
        cv2.putText(frame, str_down, (10, 90), defaults["font"], 0.5,
                    defaults["color_red"], 1, cv2.LINE_AA)

        # draw the time stamp on the frame
        timestamp = datetime.datetime.now()
        ts = timestamp.strftime("%A, %B %d, %Y - %I:%M:%S%p")
        cv2.putText(frame, ts, (10, frame.shape[0] - 10),
                    defaults["font"], 0.35, defaults["color_red"], 1)

        if args["show"] is True:
            cv2.imshow('People Counter', frame)

            # show the mask
            #cv2.imshow('Mask', mask)

        # write the mask
        if args["video_write_on"] is True:
            video_recM.write(mask)

        # write the frame after it has been processed
        if args["video_write_on"] is True:
            video_recP.write(frame)

        # pre-set ESC, Ctrl-c or 'q' to exit
        k = cv2.waitKey(30) & 0xFF
        if k == 27 or k == 99 or k == ord('q'):
            print("\nProgram terminated by user.")
            break

        # update the frame count
        fps.update()

        #trc.time_stop(mess={"line#": get_linenumber()})
        #trc.time_elapsed()

    # stop the timer and display FPS information
    fps.stop()
    print("\nProgram Stopping:\n\telapsed time: {:.2f}".format(fps.elapsed()))
    print("\tapprox. FPS: {:.2f}".format(fps.fps()))

    # do the final cleanup before exiting
    trc.stop()
    cap.stop()
    if args["video_write_on"] is True:
        video_rec.release()
        video_recP.release()
        video_recM.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':

    # update your defaults based on the box your running on
    if os.uname()[1] == "desktop":
        defaults["path"] = "/home/jeff/Videos"
    elif os.uname()[1] == "BlueRpi":
        defaults["path"] = "/home/pi/Videos"
    elif os.uname()[1] == "YellowRpi":
        defaults["path"] = "/home/pi/Videos"
    else:
        print("This program currently only works on \"desktop\" and \"BlueRpi\" ... Exiting")
        exit(1)

    # parse your command line options, arguments and, switches
    args = vars(ArgParser(defaults))

    # check to make sure your running the right version of python
    if sys.version_info[0] < 3:
        print("You must us Python 3 ... Exiting")
        exit(1)

    # check if your input files exit
    if os.path.isfile(args["file_in"]) is False:
        print("File \"" + args["file_in"] + "\" doesn't exit ... Exiting")
        exit(1)

    # create and start object to manage trace messages
    # set the frequency of the heartbeat message (in seconds)
    trc = tracemess.TraceMess(defaults["platform"], src=args["source"])
    trc.start(on=args["trace_on"])
    trc.heart_freq(60)

    # set up and down counters
    cnt_up = initials["cnt_up"]
    cnt_down = initials["cnt_down"]

    cap = vstream.VStream(source=args["source"], path=args["file_in"],
                          resolution=args["resolution"][0],
                          src=args["video_device"])

    # wait while camera warms up and VStream initialize
    time.sleep(args["warmup_time"])

    # print out your target and native resolution
    print("camera version =", cap.version())
    print("target resolution = (width, height) =", cap.target_res())
    print("native resolution = (width, height) =", cap.native_res())

    trc.info({"line#": get_linenumber(), "source": args["source"],
              "path": args["file_in"], "src": args["video_device"]})

    # Get current width and height of frame
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    if args["video_write_on"] is True:
        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'MP4V')
        fourcc = cv2.VideoWriter_fourcc('M', 'P', '4', 'V')
        fourcc = cv2.VideoWriter_fourcc(*'a\0\0\0')

        video_recP = cv2.VideoWriter(args["file_recP"],
                                     fourcc, 20.0, (int(width), int(height)))
        video_recM = cv2.VideoWriter(args["file_recM"],
                                     fourcc, 20.0, (int(width), int(height)))
        video_rec = cv2.VideoWriter(args["file_rec"],
                                    fourcc, 20.0, (int(width), int(height)))

    # enter the main loop of the video processing
    PeopleCounter(cap, args["resolution"][0],
                  initials["cnt_up"], initials["cnt_down"])
