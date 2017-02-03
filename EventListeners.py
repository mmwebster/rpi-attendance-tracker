#!/usr/bin/env python

#################################################################################
# Import libraries
#################################################################################
import threading
import time
from Event import Event
from Queue import Queue

#################################################################################
# Perform initializations
#################################################################################


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
        print("Running...")
        print("Stopped...")



#################################################################################
# House keeping..close interfaces and processes
#################################################################################
