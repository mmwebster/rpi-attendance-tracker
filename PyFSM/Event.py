#!/usr/bin/env python

#################################################################################
# Import libraries
#################################################################################
import threading
from abc import ABCMeta, abstractmethod, abstractproperty

#################################################################################
# Perform initializations
#################################################################################

#################################################################################
# Class definitions
#################################################################################
class Event():
    # event priority types
    @classmethod
    def EVENT_PRIORITY(self, name):
        priority_types = {"INIT": 1, "TIMER": 2, "HIGH": 3, "MEDIUM": 4, "LOW": 5}
        return priority_types[name]

    # Event private functions
    def __init__(self, data=None):
        self.data = data
    def __cmp__(self, other):
        return cmp(self.priority(), other.priority())

    # user defined event properties
    def name(self):
        return None
    def priority(self):
        return 0

# Default event types
class InitEvent(Event):
    def name(self):
        return "INIT"
    def priority(self):
        return Event.EVENT_PRIORITY("INIT")
class EntryEvent(Event):
    def name(self):
        return "ENTRY"
    def priority(self):
        return Event.EVENT_PRIORITY("MEDIUM")
class ExitEvent(Event):
    def name(self):
        return "EXIT"
    def priority(self):
        return Event.EVENT_PRIORITY("MEDIUM")
class TimerEvent(Event):
    def name(self):
        return "TIMER"
    def priority(self):
        return Event.EVENT_PRIORITY("TIMER")


#################################################################################
# House keeping..close interfaces and processes
#################################################################################
