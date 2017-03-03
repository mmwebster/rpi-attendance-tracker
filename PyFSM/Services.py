#!/usr/bin/env python

#################################################################################
# Import libraries
#################################################################################
import threading
import time
from os import environ as ENV

#################################################################################
# Perform initializations
#################################################################################


#################################################################################
# Class definitions
#################################################################################
# @desc A service is a process that should be run contiously and that directly
#       listens to particular event types, defined during its initialization
# @note Implementation is incomplete
class Service(threading.Thread):
    def __init__(self):
        # init the thread
        threading.Thread.__init__(self)
        # do not run as daemon to ensure that main thread waits until this thread
        # finishes before dieing
        self.setDaemon(False) # default

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

#################################################################################
# House keeping..close interfaces and processes
#################################################################################
