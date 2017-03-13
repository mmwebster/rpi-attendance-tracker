#!/usr/bin/env python

#####################################################################################
# Import libraries
#####################################################################################
import Event
import Service
from Job import Job
import EventListener
import PyFSMException
from Queue import PriorityQueue
from DropboxStorage import DropboxStorage
from LocalStorage import LocalStorage

#####################################################################################
# Class Definitions
#####################################################################################
class PyFSM():
    def __init__(self, services, eventListeners, stateHandlers, enabledLibs):
        print "Init'ing PyFSM"
        # init internals
        self.services = []
        self.eventListeners = []
        self.stateHandlers = {}
        self.enabledLibs = {}
        # add defaults
        self.jobProcessorService = Service.JobProcessorService(3)
        self.services.extend([self.jobProcessorService])
        self.eventListeners.extend(
                [EventListener.InitEventListener()])
        # add user defined
        self.services.extend(services)
        self.eventListeners.extend(eventListeners)
        for stateHandler in stateHandlers:
            self.stateHandlers[stateHandler.name()] = stateHandler

        # prepare enabled libs for state handler injection
        for class_instance in enabledLibs:
            # add dict entries <class-name> -> <class-instance>
            self.enabledLibs[str(type(class_instance).__name__)] = class_instance

        # TODO: figure out how to init this properly, given the new format

        # init current state
        print("State handlers:")
        print(str(self.stateHandlers))
        if "INIT" in self.stateHandlers:
            self.currentStateHandler = self.stateHandlers["INIT"]
        else:
            raise PyFSMException.InitializationError("No InitState defined in the stateHandlers dictionary.")

        # instantiate the event queue
        self.eventQueue = PriorityQueue() # thread-safe queue

        # startup all event listeners and services
        for eventListener in self.eventListeners:
            eventListener._set_event_queue(self.eventQueue)
            eventListener.start()
        for service in self.services:
            service._set_event_queue(self.eventQueue)
            service.start()

    # @desc Call this method to start the FSM, after initializing it. This method
    #       will only return if there's an error.
    def start(self):
        did_error = False
        # Begin the main FSM runloop
        while not did_error:
            # If there are events to process
            if not self.eventQueue.empty():
                # Fetch the highest priority event and process it
                state_return = self._run(self.currentStateHandler, self.eventQueue.get())

                # extract the error return from the handler if present
                if state_return["did_error"]:
                    did_error = True
                    error_message = state_return["error_message"]
                    break
                # extract the next state string from the returned hash
                next_state_str = state_return["next_state"]

                # if the state changed
                if not next_state_str == self.currentStateHandler.name(): #current_state_str:
                    # run current state with exit event (ignore return)
                    self._run(self.currentStateHandler, Event.ExitEvent())
                    if next_state_str in self.stateHandlers:
                        # set current state to next state
                        self.currentStateHandler = self.stateHandlers[next_state_str]
                    else:
                        raise PyFSMException.UndefinedStateError("State " + next_state_str + " is undefined.")
                    # run next state with entry event (ignore return)
                    self._run(self.currentStateHandler, Event.EntryEvent())

        # error'd out..print the message
        print("ERROR: " + error_message)
        # then return it
        return error_message

    # @desc Called internally during every tick of the state machine
    def _run(self, currentStateHandler, event):
        args = {}
        # Add default args
        args.update({ "event": event,
                      "event_queue": self.eventQueue,
                      "job_queue": self.jobProcessorService })
        # inject requested lib instances
        for lib_name in currentStateHandler.args():
            if lib_name in self.enabledLibs:
                args[lib_name] = self.enabledLibs[lib_name]
            else:
                raise PyFSMException.DisabledLibError("The requested lib \""
                        + lib_name + "\" was not enabled")
        print("ARGS:")
        print(str(args))
        # call the current state's handler function and save it's returned data
        state_return = currentStateHandler.run(args)
        return state_return
