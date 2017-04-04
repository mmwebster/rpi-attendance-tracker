#!/usr/bin/env python

# @note ENV vars: ATTENDANCE_TRACKER_TEST, and AT_LOCAL_STORAGE_PATH

#####################################################################################
# Import libraries
#####################################################################################
import Jobs
import Events
import Services
import StateHandlers
import EventListeners
from os import environ as ENV
from pyfsm.Pyfsm import Pyfsm
from pyfsm import EventListener
from Queue import PriorityQueue
from pyfsm.LocalStorage import LocalStorage
from pyfsm.DropboxStorage import DropboxStorage

#####################################################################################
# Main logic
#####################################################################################
def main():
    #################################################################################
    # Perform tests
    #################################################################################
    # Check if test mode enabled
    if not 'ATTENDANCE_TRACKER_TEST' in ENV or \
       not int(ENV['ATTENDANCE_TRACKER_TEST']) == 1:
           print "Attendance Tracker Test Mode DISABLED"
    else:
       print "Attendance Tracker Test Mode ENABLED"

    # run all lib tests
    print("MAIN: Started up! Running tests.")

    # TODOB: run tests here
    # TODOB: check if each test passed and proceed if so

    #################################################################################
    # Perform initializations
    #################################################################################
    LEDQueue = PriorityQueue() # thread-safe queue
    services = [ Services.LEDIndicatorService(LEDQueue) ]
    # services = [Services.AsyncPeriodicSyncWithDropbox(20,["time_in_entries.csv", "time_out_entries.csv", "time_entries.csv"])]
    eventListeners = [ EventListener.TimerEventListener(5.0),
                       EventListeners.CardReadEventListener("MY_CARD_READER") ]
    stateHandlers = [ StateHandlers.InitStateHandler,
                      StateHandlers.TempStateHandler ]
    if 'ATTENDANCE_TRACKER_TEST' in ENV or int(ENV['ATTENDANCE_TRACKER_TEST']) == 1:
        enabledLibs = [ LocalStorage(ENV["AT_LOCAL_STORAGE_PATH"]) ]
    else:
        # TODO: get this path from the config.csv instead, modify LocalStorage
        #       class so that it defaults to what's in config.csv if there's no param
        enabledLibs = [ LocalStorage(ENV["AT_LOCAL_STORAGE_PATH"]) ]
    # common params are passed to every state handler
    commonArgs = { "LEDQueue": LEDQueue }

    # enabledLibs = [ LocalStorage(ENV["AT_LOCAL_STORAGE_PATH"]),
    #         DropboxStorage(ENV["AT_DROPBOX_AUTH_TOKEN"], ENV["AT_LOCAL_STORAGE_PATH"])]

    #################################################################################
    # Begin the main FSM runloop
    #################################################################################
    pyfsm = Pyfsm(services, eventListeners, stateHandlers, enabledLibs, commonArgs)
    error_message = pyfsm.start()

    # error'd out..print the message
    print("ERROR: " + error_message)

if __name__ == '__main__':
    main()
