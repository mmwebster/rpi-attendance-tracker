#!/usr/bin/env python

#################################################################################
# Import libraries
#################################################################################
import time
import threading
from os import environ as ENV
from Queue import PriorityQueue

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
        self.setDaemon(True) # default

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

# Default services
class JobProcessorService(Service):
    def __init__(self, concurrency_limit):
        Service.__init__(self)
        # self.concurrency_limit = concurrency_limit
        # thread-safe queue
        self.jobQueue = PriorityQueue()
        # init p-queue w/ max number of threads to run concurrently
        self.processingQueue = PriorityQueue(concurrency_limit)

    # simple mutator to push job to queue
    def put(self, job):
        self.jobQueue.put(job)

    # lifetime of the event listener
    def run_prod(self):
        while True:
            # block until able to fetch another job for processing
            job = self.jobQueue.get(True)
            # push to processing queue if concurrency limit hasn't been reached
            name = type(job).__name__
            self.processingQueue.put(name, True)
            print("Pushed job \"" + str(name) + "\" to processing queue")
            # start it w/ internal thread wrapper to signal uppon completion
            job_wrapper = threading.Thread(target=self._process_job, args=[job])
            job_wrapper.start()

    # TODO: optimize so as to not require a wrapper thread for every thread processed
    def _process_job(self, args):
        job = args
        # start the job
        job.start()
        # wait until completion
        job.join()
        name = type(job).__name__
        print("Completed job \"" + str(name) + "\"")
        # signal processor service upon completion (by removing from processing queue)
        # currently no method for determining which particular task completed
        self.processingQueue.get()

#################################################################################
# House keeping..close interfaces and processes
#################################################################################
