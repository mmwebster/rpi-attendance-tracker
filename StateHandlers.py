#!/usr/bin/env python

#################################################################################
# Import libraries
#################################################################################
import Jobs
import time
from os import environ as ENV
from LEDIndicator import LEDIndicator
from pyfsm.StateHandler import StateHandler
from abc import abstractmethod, abstractproperty, ABCMeta

##########################################################################################
# FSM state functions
# @desc Definitions for each state of the FSM. They must return a state name
#       corresponding to the next state. Python doesn't have switch statements,
#       so using a lookup table to call the handler associated with each state.
##########################################################################################
class InitStateHandler(StateHandler):
    @classmethod
    def name(self):
        return "INIT"

    @classmethod
    def run(self, args):
        print("INIT SH processing event: " + str(args["event"].name()) + "->" + str(args["event"].data))
        if (args["event"].name() == "ENTRY"):
            # entering INIT state
            return { "did_error": False }
        elif (args["event"].name() == "INIT"):
            # processing INIT event
            # indicate startup
            args["common_args"]["LEDQueue"].put(LEDIndicator.LED_TYPES[1])
            time.sleep(2)
            return { "next_state": "TEMP", "did_error": False }
        elif (args["event"].name() == "TIMER"):
            # processing INIT event
            return { "next_state": "INIT", "did_error": False }
        elif (args["event"].name() == "EXIT"):
            # exiting INIT state
            return { "did_error": False }
        else:
            return { "next_state": "INIT", "did_error": False }

class TempStateHandler(StateHandler):
    @classmethod
    def name(self):
        return "TEMP"

    @classmethod
    def args(self):
        # return [ "LocalStorage", "DropboxStorage" ]
        return [ "LocalStorage" ]

    @classmethod
    def run(self, args):
        print("TEMP SH processing event: " + str(args["event"].name()) + "->" + str(args["event"].data))
        if (args["event"].name() == "ENTRY"):
            # entering TEMP state
            # indicate system ready
            args["common_args"]["LEDQueue"].put(LEDIndicator.LED_TYPES[0])
            return { "did_error": False }
        elif (args["event"].name() == "TIMER"):
            # processing TEMP event
            return { "next_state": "TEMP", "did_error": False}
        elif (args["event"].name() == "CARD_READ"):
            # asyncronously write entry to the USB stick
            args["job_queue"].put(Jobs.AsyncWriteTimeEntryJob(args["event"].data, args["LocalStorage"]))
            return { "next_state": "TEMP", "did_error": False }
        elif (args["event"].name() == "EXIT"):
            # exiting INIT state
            return { "did_error": False }
        else:
            return { "did_error": True, "error_message": "Invalid event" }
