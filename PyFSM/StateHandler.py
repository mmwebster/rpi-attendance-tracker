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
# @note User MUST define a state handler with the name "INIT"
class StateHandler(object):
    # __metaclass__ = ABCMeta

    # @note USER DEFINED
    # @desc Must return an array of string corresponding to the names of all libs
    #       to be passed to the state handler's run method as arguments
    @classmethod
    def name(self):
        return None

    # @note USER DEFINED
    # @desc Must return an array of string corresponding to the names of all libs
    #       to be passed to the state handler's run method as arguments
    @classmethod
    def args(self):
        return None

    # @note USER DEFINED
    # @desc Must accept an args paramater that contains a dictionary of every
    #       argument passed. All state handlers are passed the "event" argument
    #       of type Event, along with the other args requested in the abstract args
    #       property class definition
    # @return A dictionary containing keys for `next_state` (the identifier of the
    #         next state to be transitioned to) and `did_error`. If `did_error` is
    #         `True`, then the key `error_message` should also be defined. If
    #         returning `did_error` as `True`, then the `next_state` need not be
    #         returned as well (the FSM will error out anyway). If handling the
    #         `ENTRY` or `EVENT`, the `next_state` need not be defined, as this
    #         event is generated internally and the whatever transition that
    #         prompted the generation of the event will persist.
    @classmethod
    def run(self, args):
        return None

#################################################################################
# Example init/startup state
#################################################################################
# class InitState(StateHandler):
#     @abstractproperty
#     def name(self):
#         return "INIT"
#
#     @abstractproperty
#     def args(self):
#         return [ "LocalStorage", "DropboxStorage"]
#
#     @abstractmethod
#     def run(self, args):
#         if (args["event"].name == "ENTRY"):
#             # entering INIT state
#             return { "did_error": False }
#         elif (args["event"].name == "INIT"):
#             # processing INIT event
#             return { "next_state": "MY_SECOND_STATE", "did_error": False }
#         elif (args["event"].name == "EXIT"):
#             # exiting INIT state
#             return { "did_error": False }
#         else:
#             return { "did_error": }

#################################################################################
# House keeping..close interfaces and processes
#################################################################################
