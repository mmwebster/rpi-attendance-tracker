#!/usr/bin/env python

#################################################################################
# Import libraries
#################################################################################
import threading
import time
import Event
from Queue import Queue

#################################################################################
# Perform initializations
#################################################################################


#################################################################################
# Class definitions
#################################################################################
class EventListener(threading.Thread):
    def __init__(self, eventQueue):
        # init the thread and run as daemon to kill it when the main thread dies
        threading.Thread.__init__(self, daemon=True)
        self.eventQueue = eventQueue

class CardReader(EventListener):
    def __init__(self, eventQueue, period, device_name):
        EventListener.__init__(self, eventQueue)
        self.period = period
        self.device_name = device_name

    # lifetime of the event listener
    def run(self):
        print("Running...")
        print("Stopped...")

class Timer(EventListener):
    def __init__(self, eventQueue, period):
        EventListener.__init__(self, eventQueue)
        self.period = period

    # lifetime of the event listener
    def run(self):
        while True:
            time.sleep(self.period)
            self.eventQueue.put(Event.Event(
                Event.EVENT_PRIORITIES["TIMER"], {"name": "Timer Event (" + str(self.period) + ")"}
                ))

# Posts an init event immediately, then dies
class Init(EventListener):
    def __init__(self, eventQueue):
        EventListener.__init__(self, eventQueue)

    # lifetime of the event listener
    def run(self):
        self.eventQueue.put(Event.Event(
            Event.EVENT_PRIORITIES["INIT"], {"name": "Init"}
            ))


#################################################################################
# House keeping..close interfaces and processes
#################################################################################
