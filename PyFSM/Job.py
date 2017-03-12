#!/usr/bin/env python

#################################################################################
# Import libraries
#################################################################################
import threading
import time
from DropboxStorage import DropboxStorage
from datetime import datetime
from os import environ as ENV

#################################################################################
# Perform initializations
#################################################################################


#################################################################################
# Utility functions
#################################################################################
# @note Currently does not operate with a queue, just start the job immediately
#       don't yet know if there would be any benefit to only allowing 1 job to
#       run at a time
def queue(job):
    job.start()

#################################################################################
# Class definitions
#################################################################################
# @desc Jobs are created for one-off tasks in order to maintain clean
#       thread abstractions for different purposes. Jobs also make it easier to
#       limit the load on the CPU when having multiple processes running. By
#       setting the concurrencyLimit paramater, you can control how many jobs are
#       processed concurrently, and therefore the load on the CPU from processing
#       jobs. The default concurrency limit is -1, which disables queuing and
#       executes jobs as soon as they come in.
class Job(threading.Thread):
    def __init__(self):
        # init the thread
        threading.Thread.__init__(self)
        # do not run as daemon to ensure that main thread waits until this thread
        # finishes before dieing
        self.setDaemon(False) # default, main thread must wait for completion

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
