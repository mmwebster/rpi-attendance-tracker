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

# @desc When the job is started, it creates a time entry for the user stored in
#       `card_event_data` and appends it local storage (USB stick)
class AsyncWriteTimeEntry(Job):
    def __init__(self, card_event_data, localStorage):
        Job.__init__(self)
        self.student_id = card_event_data["id"]
        self.localStorage = localStorage

    def run_prod(self):
        name = self.localStorage.read_config_value(str(self.student_id))
        print("Running... with " + str(name))
        return

#################################################################################
# House keeping..close interfaces and processes
#################################################################################
