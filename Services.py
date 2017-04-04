#!/usr/bin/env python

#################################################################################
# Import libraries
#################################################################################
from time import sleep
from os import environ as ENV
if not 'ATTENDANCE_TRACKER_TEST' in ENV or \
       not int(ENV['ATTENDANCE_TRACKER_TEST']) == 1:
    import RPi.GPIO as GPIO
from pyfsm.Service import Service
from LEDIndicator import LEDIndicator

#################################################################################
# Perform initializations
#################################################################################

#################################################################################
# Class definitions
#################################################################################
# Default services
# @desc A lightweight state machine to drive the LED Indicator by listening for
#       new LED requests from the LEDQueue
# @param LEDQueue A reference to an instance of a queue that will contain new
#        requests for the LED color and the blink number (code)
# @note The LED state does not correspond to the FSM state, LED indicator states
#       are listed in Jobs.py
class LEDIndicatorService(Service):
    def __init__(self, LEDQueue):
        Service.__init__(self)
        # self.concurrency_limit = concurrency_limit
        # thread-safe queue
        self.LEDQueue = LEDQueue
        self.current_color_pin = None
        self.current_blinks = 0 # default to solid
        self.fsm_iterator = 0
        # intialize pins
        if not 'ATTENDANCE_TRACKER_TEST' in ENV or \
                not int(ENV['ATTENDANCE_TRACKER_TEST']) == 1:
            GPIO.setwarnings(False) # ignore channel-open warnings
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(LEDIndicator.RLED_PIN, GPIO.OUT)
            GPIO.setup(LEDIndicator.GLED_PIN, GPIO.OUT)
            GPIO.setup(LEDIndicator.BLED_PIN, GPIO.OUT)

    # lifetime of the event listener
    def run_prod(self):
        current_state = "init"
        led_type = None
        while True:
            # TODO: remove redunancies in the following two blocks
            # reset with new vals if a new LED Indicator state is requested
            if not self.LEDQueue.empty():
                led_type = self.LEDQueue.get(False)
                self.current_color_pin = led_type["color"]
                self.current_blinks = led_type["blinks"]
                current_state = "init"

            # if the LED Indicator has never received a type, block until it does
            if led_type == None:
                if not 'ATTENDANCE_TRACKER_TEST' in ENV or \
                        not int(ENV['ATTENDANCE_TRACKER_TEST']) == 1:
                    print("LEDIndicator: Blocking LED Indicator thread until receiving the first type")
                led_type = self.LEDQueue.get(True)
                self.current_color_pin = led_type["color"]
                self.current_blinks = led_type["blinks"]
                current_state = "init"

            # execute next iteration of LED state
            next_state = self.run_state(current_state)
            current_state = next_state

    def run_state(self, current_state):
        # init next state
        next_state = None
        # service function of current state and return next state
        if current_state == "init":
            self.fsm_iterator = 0
            # set all LEDs to LOW
            if not 'ATTENDANCE_TRACKER_TEST' in ENV or \
                    not int(ENV['ATTENDANCE_TRACKER_TEST']) == 1:
                for colorPin in [LEDIndicator.RED, LEDIndicator.GREEN, LEDIndicator.BLUE]:
                    GPIO.output(self.current_color_pin, GPIO.LOW)
            else:
                print("LEDIndicator: Turning all LEDs off")
            # transition to off state
            next_state = "on"
        elif current_state == "waiting":
            # 1s between .5s blinks where blink number is greater than 1
            if not 'ATTENDANCE_TRACKER_TEST' in ENV or \
                    not int(ENV['ATTENDANCE_TRACKER_TEST']) == 1:
                print("LEDIndicator: Waiting...")
            sleep(1)
            next_state = "on"
        elif current_state == "on":
            if not 'ATTENDANCE_TRACKER_TEST' in ENV or \
                    not int(ENV['ATTENDANCE_TRACKER_TEST']) == 1:
                GPIO.output(self.current_color_pin, GPIO.HIGH)
            else:
                print("LEDIndicator: Turning an LED on, with LED_TYPE == " + str(self.current_blinks))
            if self.current_blinks == 0:
                # always stay ON if blinks == 0
                next_state = "on"
            else:
                next_state = "off"
            sleep(.5)
        elif current_state == "off":
            # inc iterator
            self.fsm_iterator += 1
            if not 'ATTENDANCE_TRACKER_TEST' in ENV or \
                    not int(ENV['ATTENDANCE_TRACKER_TEST']) == 1:
                GPIO.output(self.current_color_pin, GPIO.LOW)
            else:
                print("LEDIndicator: Turning an LED off")
            if self.fsm_iterator < self.current_blinks:
                next_state = "on"
            elif self.current_blinks == 1:
                # always cycle between .5s OFF/ON for blinks == 1
                self.fsm_iterator = 0
                next_state = "on"
            else:
                # perform .5s OFF/ON, then 1s wait for blinks > 1
                self.fsm_iterator = 0
                next_state = "waiting"
            sleep(.5)
        else:
            print("LEDIndicator: ERROR: Invalid state passed as current_state ->" + str(current_state))
            sleep(.5)

        return next_state

    # close all used GPIO ports
    def __del__(self):
        print("LEDIndicator: Cleaning up GPIO")
        GPIO.cleanup()

#################################################################################
# House keeping..close interfaces and processes
#################################################################################
