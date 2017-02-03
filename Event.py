#!/usr/bin/env python

#################################################################################
# Import libraries
#################################################################################
import threading
from abc import ABCMeta, abstractmethod, abstractproperty

#################################################################################
# Perform initializations
#################################################################################
EVENT_PRIORITIES = {"INIT": 1, "TIMER": 2, "HIGH": 3, "MEDIUM": 4, "LOW": 5}
EVENT_NAME = 0
EVENT_PRIORITY = 1

#################################################################################
# Class definitions
#################################################################################
class Event():
    # abstract public event types
    @abstractproperty
    def EVENTS(self):
        pass
    EVENTS = {
        "INIT": ("INIT", EVENT_PRIORITIES["INIT"]),
        "TIMER": ("TIMER", EVENT_PRIORITIES["TIMER"]),
        "ENTRY": ("ENTRY", EVENT_PRIORITIES["HIGH"]),
        "EXIT": ("EXIT", EVENT_PRIORITIES["HIGH"]),
        "CARD_READ": ("CARD_READ", EVENT_PRIORITIES["MEDIUM"]),
    }

    # Event private functions
    def __init__(self, event, data=None):
        self.priority = event[EVENT_PRIORITY]
        self.name = event[EVENT_NAME]
        self.data = data
    def __cmp__(self, other):
        return cmp(self.priority, other.priority)

    # Event pub functions
    def name(self):
        return self.name

#################################################################################
# House keeping..close interfaces and processes
#################################################################################
