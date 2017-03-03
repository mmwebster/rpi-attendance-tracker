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

# @desc When the job is started, it creates a time entry for the user stored in
#       `card_event_data` and appends it local storage (USB stick)
# @TODO Make it so that only one of these workers can be running at a time, to ensure
#       shared csv data is not corrupted. Can also lock objects, but easiest way is to
#       implement job queue allowing only one job to run at a time
class AsyncWriteTimeEntry(Job):
    def __init__(self, card_event_data, localStorage):
        Job.__init__(self)
        self.student_id = card_event_data["id"]
        self.localStorage = localStorage

    def run_prod(self):
        name = self.localStorage.read_config_value(str(self.student_id))
        epoch = time.time()
        timestamp = datetime.fromtimestamp(epoch).strftime('%Y-%m-%d %H:%M:%S')

        # write time entries dependent on student's clock in/out state
        if (str(self.student_id) in self.localStorage.time_in_entries):
            # time entry started, close it out
            # write the "out" entry
            out_entry = [[name, self.student_id, timestamp]]
            self.localStorage.append_rows("time_out_entries.csv", out_entry)
            print("Appended Out entry: " + str(out_entry))
            prev_entry = self.localStorage.time_in_entries[str(self.student_id)]
            # write the "in/out" entry
            elapsed_hours = round(((epoch - prev_entry["epoch_in"]) / 60), 2)
            in_out_entry = \
                [[name, self.student_id, prev_entry["ts_in"], timestamp, elapsed_hours]]
            self.localStorage.append_rows("time_entries.csv", in_out_entry)
            # remove "in" entry from the localStorage hash
            del self.localStorage.time_in_entries[str(self.student_id)]
            print("Appended In/Out entry: " + str(in_out_entry))
        else:
            # now previous entry, start a new one
            # write the "in" entry
            in_entry = [[name, self.student_id, timestamp]]
            self.localStorage.append_rows("time_in_entries.csv", in_entry)
            # add "in" entry to hash
            self.localStorage.time_in_entries[str(self.student_id)] = \
                {"epoch_in": epoch, "ts_in": timestamp}
            print("Appended In entry: " + str(in_entry))

# TODO: this should be paired with a service, jobs are one-off
class AsyncPeriodicSyncWithDropbox(Job):
    # @param period Time in seconds to wait between syncs
    def __init__(self, period, file_names):
        Job.__init__(self)
        self.period = period
        self.file_names = file_names
        # necessary since in inf. loop, temporary until ported to service
        self.setDaemon(True)

    def run_prod(self):
        dbx = DropboxStorage(ENV["AT_DROPBOX_AUTH_TOKEN"], ENV["AT_LOCAL_STORAGE_PATH"])
        while True:
            # wait for `period` to run
            time.sleep(self.period)
            # log it
            print("Syncing with dropbox")
            # sync all of self.files
            for file_name in self.file_names:
                dbx.upload(file_name)


#################################################################################
# House keeping..close interfaces and processes
#################################################################################
