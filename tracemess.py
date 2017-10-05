#
# Maintainer:   jeffskinnerbox@yahoo.com / www.jeffskinnerbox.me
# Version:      0.2.0

from cv2 import __version__
import uuid
import json
import ts_dweepy        # https://pypi.python.org/pypi/dweepy/
import time
import datetime
from inspect import currentframe, getframeinfo  # https://stackoverflow.com/questions/3056048/filename-and-line-number-of-python-script


def get_linenumber():
    cf = currentframe()
    return cf.f_back.f_lineno


class TraceMess:

    def __init__(self, on=True, verbose=False, src="not specified"):
        self.run_stamp = {
            "mess-type": "EXEC",
            "mess-format": "0.0.2",
            "run-id": str(uuid.uuid4()),
            "run-time": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
            "run-status": "init",
            "run-platform": "Desktop-Jupyter",
            "run-source": src,
            "verbose": verbose,
            "timer-start": None,
            "timer-stop": None,
            "version": {
                "algorithm": "0.0.3",
                "cv2": __version__
            }
        }

    def start(self, on=True):
        if on is False:
            return self

        self.run_stamp["run-status"] = "start"
        self.run_stamp["run-time"] = time.strftime("%Y-%m-%d %H:%M:%S",
                                                   time.gmtime())
        if self.run_stamp["verbose"] is True:
            print(json.dumps(self.run_stamp))
        else:
            print(json.dumps({"INFO": {"trace started": self.run_stamp["run-time"]}}))

        return self

    def stop(self, on=True):
        if on is False:
            return

        self.run_stamp["run-status"] = "stop"
        self.run_stamp["run-time"] = time.strftime("%Y-%m-%d %H:%M:%S",
                                                   time.gmtime())
        if self.run_stamp["verbose"] is True:
            print(json.dumps(self.run_stamp))
        else:
            print(json.dumps({"INFO": {"trace stopped": self.run_stamp["run-time"]}}))

    def time_start(self, on=True, mess=None):
        if on is False:
            return

        # start the timer
        self.run_stamp["timer-start"] = datetime.datetime.now()
        t= time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

        if self.run_stamp["verbose"] is True:
            print(json.dumps({"mess-type": "INFO",
                            "run-id": self.run_stamp["run-id"],
                            "timer-start": t, "mess-text": mess}))
        else:
            print(json.dumps({"INFO": {"timer-start": t, "mess-text": mess}}))

    def time_stop(self, on=True, mess=None):
        if on is False:
            return

        # stop the timer
        self.run_stamp["timer-stop"] = datetime.datetime.now()
        t= time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

        if self.run_stamp["verbose"] is True:
            print(json.dumps({"mess-type": "INFO",
                            "run-id": self.run_stamp["run-id"],
                            "timer-stop": t, "mess-text": mess}))
        else:
            print(json.dumps({"INFO": {"timer-stop": t, "mess-text": mess}}))

    def time_elapsed(self, on=True, mess=None):
        if on is False:
            return

        # return the total number of seconds between the start and end interval
        t = (self.run_stamp["timer-stop"] - self.run_stamp["timer-start"]).total_seconds()

        if self.run_stamp["verbose"] is True:
            print(json.dumps({"mess-type": "INFO",
                            "run-id": self.run_stamp["run-id"],
                            "timer-interval": t,
                            "mess-text": mess}))
        else:
            print(json.dumps({"INFO": {"timer-interval": t,
                "mess-text": mess}}))

    def info(self, mess, on=True):
        if on is False:
            return

        if self.run_stamp["verbose"] is True:
            print(json.dumps({"mess-type": "INFO",
                            "run-id": self.run_stamp["run-id"],
                            "mess-text": mess}))
        else:
            print(json.dumps({"INFO": mess}))

    def error(self, mess, on=True):
        if on is False:
            return

        if self.run_stamp["verbose"] is True:
            print(json.dumps({"mess-type": "ERROR",
                            "run-id": self.run_stamp["run-id"],
                            "mess-text": mess}))
        else:
            print(json.dumps({"ERROR": mess}))

    def warning(self, mess, on=True):
        if on is False:
            return

        if self.run_stamp["verbose"] is True:
            print(json.dumps({"mess-type": "WARNING",
                            "run-id": self.run_stamp["run-id"],
                            "mess-text": mess}))
        else:
            print(json.dumps({"WARNING": mess}))


    def feature(self, mess, on=True):
        if on is True:
            if self.run_stamp["verbose"] is True:
                print(json.dumps({"mess-type": "FEATURE",
                                "run-id": self.run_stamp["run-id"],
                                "mess-text": mess}))
            else:
                print(json.dumps({"FEATURE": mess}))

        ts_dweepy.dweet_for(self.run_stamp["run-platform"],
                            {"mess-type": "FEATURE",
                             "run-id": self.run_stamp["run-id"],
                             "mess-text": mess})
