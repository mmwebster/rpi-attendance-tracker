#!/usr/bin/env python

#################################################################################
# Import libraries
#################################################################################
# Universal imports
import time
import math
import Event
import threading
from Queue import Queue
from os import environ as ENV

#################################################################################
# Perform initializations
#################################################################################

#################################################################################
# Class definitions
#################################################################################
class EventListener(threading.Thread):
    def __init__(self):
        # init the thread
        threading.Thread.__init__(self)
        # run as daemon to kill it when the main thread dies
        self.setDaemon(True)
        self.eventQueue = None

    # @desc Lifetime of the event listener, overriding Thread's def. Reads in the
    #       ENV var $ATTENDACE_TRACKER_TEST to run in test mode if the system was
    #       configured to do so.
    def run(self):
        # run event listeners in their test mode if available
        if 'ATTENDANCE_TRACKER_TEST' in ENV:
            if int(ENV['ATTENDANCE_TRACKER_TEST']) == 1:
                self.run_test()
                return # exit once completed (don't run prod version)
        # otherwise, run event listeners in their production mode
        # print "Running in prod mode"
        self.run_prod()

    # @desc Default test implementation (where otherwise undefined) that simply
    #       calls the prod implementation (that is required)
    def run_test(self):
        self.run_prod()

    def _set_event_queue(self, eventQueue):
        self.eventQueue = eventQueue


# Posts an init event immediately, then dies
# Default event Listeners
class InitEventListener(EventListener):
    def __init__(self):
        EventListener.__init__(self)

    def run_prod(self):
        self.eventQueue.put(Event.InitEvent())

# @desc Period timer that posts a timer event
class TimerEventListener(EventListener):
    def __init__(self, period):
        EventListener.__init__(self)
        self.period = period

    # lifetime of the event listener
    def run_prod(self):
        while True:
            time.sleep(self.period)
            self.eventQueue.put(Event.TimerEvent({"period": self.period}))


#################################################################################
# House keeping..close interfaces and processes
#################################################################################
