#!/usr/bin/env python

#################################################################################
# Import libraries
#################################################################################
from pyfsm.Event import Event

#################################################################################
# Perform initializations
#################################################################################

#################################################################################
# Class definitions
#################################################################################
class CardReadEvent(Event):
    def name(self):
        return "CARD_READ"
    def priority(self):
        return Event.EVENT_PRIORITY("MEDIUM")

class ShutdownEvent(Event):
    def name(self):
        return "SHUTDOWN"
    def priority(self):
        return Event.EVENT_PRIORITY("MEDIUM")

#################################################################################
# House keeping..close interfaces and processes
#################################################################################
