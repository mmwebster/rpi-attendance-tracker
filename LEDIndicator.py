#!/usr/bin/env python

#################################################################################
# Import libraries
#################################################################################

#################################################################################
# Perform initializations
#################################################################################

#################################################################################
# Class definitions
#################################################################################
# Default services
# @note The LED state does not correspond to the FSM state, LED indicator states
#       are listed in Jobs.py
class LEDIndicator(object):
    RLED_PIN = 17
    GLED_PIN = 27
    BLED_PIN = 22
    # TODO: change these colors to arrays of the colors composing them, to support
    #       additional colors
    RED = RLED_PIN
    GREEN = GLED_PIN
    BLUE = BLED_PIN
    LED_TYPES = [
        {"color": GREEN, "blinks": 0, "message": "The system is functioning properly and ready for a card swipe."},
        {"color": GREEN, "blinks": 1, "message": "The system is starting up and not yet ready for a card swipe."},
        {"color": BLUE, "blinks": 0, "message": "The system is off and power can be safely disconnected."},
        {"color": BLUE, "blinks": 1, "message": "The system is being turned off; do not yet disconnecte from power source."},
        {"color": RED, "blinks": 2,
            "message": "Missing USB storage device; the device is either not plugged in to the RPi, or is not named \"USB-STORAGE\""},
        {"color": RED, "blinks": 3,
            "message": "Missing configure file; there is no config.csv at the top level of the USB storage device."},
        {"color": RED, "blinks": 4,
            "message": "Required configure key is undefined; make sure that all required keys are defined in the config.csv file"},
        {"color": RED, "blinks": 5,
            "message": "Unable to connect to the network; make sure that Wifi is configured properly or that Ethernet is supplied"},
        {"color": RED, "blinks": 6,
            "message": "Generic value error (check the logs in errors.csv for the exact key that was misconfig- ured)"},
        {"color": RED, "blinks": 7, "message": "Unable to authenticate with Dropbox; the provided access token was invalid"},
        {"color": GREEN, "blinks": 2, "message": "The system is starting up and not yet ready for a card swipe."} # 10
        ]

    # just a tool for readability
    states = ["init", "waiting", "off", "on"]

#################################################################################
# House keeping..close interfaces and processes
#################################################################################
