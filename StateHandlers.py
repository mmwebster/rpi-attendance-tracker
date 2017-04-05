#!/usr/bin/env python

#################################################################################
# Import libraries
#################################################################################
import Jobs
import time
import urllib
from Piezo import Piezo
from os import environ as ENV
from LEDIndicator import LEDIndicator
from pyfsm.StateHandler import StateHandler
from abc import abstractmethod, abstractproperty, ABCMeta

# all import specifically for production env (not test)
if not 'ATTENDANCE_TRACKER_TEST' in ENV or \
   not int(ENV['ATTENDANCE_TRACKER_TEST']) == 1:
    import wifi

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
    def args(self):
        # return [ "LocalStorage", "DropboxStorage" ]
        return [ "LocalStorage" ]

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
            # if no in test ENV
            if not 'ATTENDANCE_TRACKER_TEST' in ENV or \
               not int(ENV['ATTENDANCE_TRACKER_TEST']) == 1:
                # attempt to connect to the network if no network connection is present
                # determine if already connected to a network
                try:
                    urllib.urlopen("http://google.com")
                    print("Already connected to a network")
                except:
                    # not already connect to a network, try to connect
                    # connect to the wifi if no current connection
                    try:
                    ret_val = connect_to_wifi(
                                args["LocalStorage"].read_config_value('wifi-ssid'),
                                args["LocalStorage"].read_config_value('wifi-password')
                                )
                    if ret_val == False:
                        print("Specified network is out of range")
                    else:
                        print("Something else went wrong...")
                    #except:
                    #    # either the network is out
                    #    print("Specified network password is invalid or another error has occured")
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
            # beep the piezo
            args["common_args"]["PiezoQueue"].put(Piezo.BEEP_TYPES[1])
            # asyncronously write entry to the USB stick
            args["job_queue"].put(Jobs.AsyncWriteTimeEntryJob(args["event"].data, args["LocalStorage"]))
            return { "next_state": "TEMP", "did_error": False }
        elif (args["event"].name() == "EXIT"):
            # exiting INIT state
            return { "did_error": False }
        else:
            return { "did_error": True, "error_message": "Invalid event" }

##########################################################################################
# Utility functions
##########################################################################################
def connect_to_wifi(configured_ssid, configured_password):
    # find all available networks
    networks = wifi.Cell.all('wlan0')
    # determine if any ssids match that specified in the config file
    for network in networks:
        if network.ssid == configured_ssid:
            scheme_lookup = wifi.Scheme.find('wlan0', network.ssid)
            # determine if a scheme has already been created for this ssid
            if not scheme_lookup == None:
                print("Found a scheme for network ssid=" + str(network.ssid))
                return scheme_lookup.activate()
            else:
                print("Could not find a scheme for network ssid=" + configured_ssid)
                new_scheme = wifi.Scheme.for_cell('wlan0', configured_ssid, network, configured_password)
                new_scheme.save()
                return new_scheme.activate()

    # found no matching ssids, print the corresponding error code permanently
    print("Could not connect to a network, the network with the configured ssid is not in range.")
    return False
