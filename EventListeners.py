#!/usr/bin/env python

#################################################################################
# Import libraries
#################################################################################
import threading
import time
from Event import Event
from Queue import Queue
import evdev # lib for keyboard input event detection

#################################################################################
# Perform initializations
#################################################################################
KEY_STATE_DOWN = 1
KEY_STATE_UP = 0
VALID_KEY_HASH = {
    "KEY_0": 0,
    "KEY_1": 1,
    "KEY_2": 2,
    "KEY_3": 3,
    "KEY_4": 4,
    "KEY_5": 5,
    "KEY_6": 6,
    "KEY_7": 7,
    "KEY_8": 8,
    "KEY_9": 9
}


#################################################################################
# Class definitions
#################################################################################
class EventListener(threading.Thread):
    def __init__(self, eventQueue):
        # init the thread
        threading.Thread.__init__(self)
        # run as daemon to kill it when the main thread dies
        self.setDaemon(True)
        self.eventQueue = eventQueue

# Posts an init event immediately, then dies
class Init(EventListener):
    def __init__(self, eventQueue):
        EventListener.__init__(self, eventQueue)

    # lifetime of the event listener
    def run(self):
        self.eventQueue.put(Event(Event.EVENTS["INIT"]))

class Timer(EventListener):
    def __init__(self, eventQueue, period):
        EventListener.__init__(self, eventQueue)
        self.period = period

    # lifetime of the event listener
    def run(self):
        while True:
            time.sleep(self.period)
            self.eventQueue.put(Event(
                Event.EVENTS["TIMER"], {"period": self.period}
                ))

class CardReader(EventListener):
    def __init__(self, eventQueue, period, device_name):
        EventListener.__init__(self, eventQueue)
        self.period = period
        self.device_name = device_name

    # lifetime of the event listener
    def run(self):
        while True:
            # scan for devices
            devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
            # find card reader device
            if (len(devices) > 0):
                print("Input event devices available ("
                        + str(len(devices)) + "). Devices are: ")
                # init card reader discovery bool
                discovered_card_reader = False
                # display input devices
                for i, device in enumerate(devices):
                    print("    " + str(i) + ") (" + device.fn + ", "
                            + device.name + ", " + device.phys + ")")
                    # search for card reader by its name, "HID c216:0180"
                    if str(device.name) == "HID c216:0180":
                        print("Discovered card reader..listening for events \
                                until test harness is closed.")
                        # rename device for readability
                        card_reader = device
                        # indefinitely listen for events
                        byte_count = 0
                        for event in card_reader.read_loop():
                            if event.type == evdev.ecodes.EV_KEY:
                                event_key_state = evdev.util.categorize(event).keystate
                                keycode_str = evdev.util.categorize(event).keycode
                                if byte_count < 7:
                                    if event_key_state == KEY_STATE_DOWN and keycode_str in VALID_KEY_HASH:
                                        keycode_int = VALID_KEY_HASH[keycode_str]
                                        if byte_count == 0:
                                            print "ID: ",
                                        print str(keycode_int),
                                        byte_count += 1
                                        # add newline
                                        if byte_count == 7:
                                            print("")
                                if event_key_state == KEY_STATE_UP and keycode_str == "KEY_ENTER":
                                    # last byte in card, so reset byte count
                                    byte_count = 0

                # error out if unable to find card reader
                if not discovered_card_reader:
                    print("ERROR: Unable to find the card reader")
                    time.sleep(period)




#################################################################################
# House keeping..close interfaces and processes
#################################################################################
