#!/usr/bin/python3
#
# Maintainer:   jeffskinnerbox@yahoo.com / www.jeffskinnerbox.me
# Version:      0.3.0
#
# USAGE:
#     python3 monitor_ts.py                   latch onto ThingSpace and print dweet messages as they arrive  #noqa
#     python3 monitor_ts.py -f                pretty print the dweet messages                                #noqa
#     python3 monitor_ts.py -t <thing_name>   listen for <thing_name> dweet messages                         #noqa
#
# SOURCES:
#    https://pypi.python.org/pypi/dweepy/
#    https://github.com/jeffskinnerbox/ts_dweepy


import os
import json
import time
import argparse
import ts_dweepy


class Monitor():
    def __init__(self, thing, pp=False):
        self.monitor_on = False
        self.pretty_print_on = pp
        self.thing_name = thing
        self.last_mess = None
        self.polling_time = 0.25

    def start(self):
        self.monitor_on = True
        print('Starting ThingSpace Dweet monitor for the thing object \"'
              + self.thing_name + '\" ....')

    def stop(self):
        self.monitor_on = False
        print('Stopping ThingSpace Dweet monitor for the thing object \"'
              + self.thing_name + '\".')

    def format(self, pp=True):
        self.pretty_print_on = pp

    def get(self):
        """Retrieve all the messages sent so far this thing"""
        if self.monitor_on is True:
            if self.pretty_print_on is True:
                print(json.dumps(ts_dweepy.get_dweet_for(self.thing_name),
                                 indent=4, sort_keys=True))
            else:
                print(ts_dweepy.get_dweets_for(self.thing_name))

    def get_latest(self):
        """Retrieve the last messages sent for this thing"""
        if self.monitor_on is True:
            if self.pretty_print_on is True:
                print(json.dumps(ts_dweepy.get_latest_dweet_for(self.thing_name),
                                 indent=4, sort_keys=True))
            else:
                print(ts_dweepy.get_latest_dweet_for(self.thing_name))

    def listen(self):
        """Listen for a new message for this thing"""
        if self.monitor_on is True:
            while True:
                mess = ts_dweepy.get_latest_dweet_for(self.thing_name)
                if mess[0]["created"] != self.last_mess:
                    self.last_mess = mess[0]["created"]
                    if self.pretty_print_on is True:
                        print(json.dumps(ts_dweepy.get_latest_dweet_for(self.thing_name),
                              indent=4, sort_keys=True))
                    else:
                        print(ts_dweepy.get_latest_dweet_for(self.thing_name))
                time.sleep(self.polling_time)


def ArgParser():
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser(description='Utility to monitor for feature \
                                 messages being sent to ThingSpace')

    # switches actions - store_true / store_false
    ap.add_argument("-f", "--format_json",
                    help="turn on pretty print for the JSON messages",
                    action='store_true',
                    required=False,
                    default=False)

    # store actions - single parameter
    ap.add_argument("-t", "--thing_name",
                    help="provide the thing name you are monitoring",
                    action='store',
                    required=False,
                    default=os.uname()[1])

    return ap.parse_args()


if __name__ == '__main__':

    # parse the command line arguments
    args = vars(ArgParser())

    # create the thingspace monitoring object and start monitoring
    mon = Monitor(args["thing_name"], pp=args["format_json"])
    mon.start()

    # listen for the arrival of messages and then print them
    mon.listen()
