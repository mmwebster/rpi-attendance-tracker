#!/usr/bin/env python

#####################################################################################
# Import libraries
#####################################################################################
from PyFSMException import InitializationError
from Job import Job
from Service import Service
from EventListener import EventListener
from Event import Event
from Queue import PriorityQueue

# TODO: create a dictionary of state handlers based on their "name" abstract property during init of PyFSM


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
        self.enabledLibs = enabledLibs
        # add defaults
        self.eventListeners.extend(
                [EventListener.InitEventListener, EventListener.TimerEventListener])
        # add user defined
        self.services.extend(services)
        self.eventListeners.extend(eventListeners)
        for stateHandler in stateHandlers:
            self.stateHandlers[stateHandler.name] = stateHandler

        # TODO: figure out how to init this properly, given the new format

        # init current state
        if "INIT" in stateHandlers:
            self.currentState = stateHandlers["INIT"]
        else:
            print("ERROR: No InitState defined in the stateHandlers dictionary.")
            raise InitializationError("No InitState defined in the stateHandlers dictionary.")

        # instantiate the event queue
        self.eventQueue = PriorityQueue() # thread-safe queue

    # @desc Call this method to start the FSM, after initializing it. This method
    #       will only return if there's an error.
    def start(self):
        did_error = False
        # Begin the main FSM runloop
        while not did_error:
            # If there are events to process
            if not eventQueue.empty():
                # Fetch the highest priority event and process it
                state_return = self._run(current_state_handler, eventQueue.get(), localStorage)
                # extract the next state string from the returned hash
                next_state_str = state_return["next_state"]
                # extract the error return from the handler if present
                if state_return["did_error"]:
                    didError = True
                    error_message = state_return["error_message"]

                # set the next state function using the returned next state str
                next_state_handler = state_handlers[next_state_str]

                # if the state changed
                if not next_state_str == current_state_str:
                    # run current state with exit event (ignore return)
                    self._run(current_state_handler, Event(Event.EVENTS["EXIT"]), localStorage)
                    # run next state with entry event (ignore return)
                    self._run(next_state_handler, Event(Event.EVENTS["ENTRY"]), localStorage)

                # set current state to next
                current_state_handler = next_state_handler
                current_state_str = next_state_str

        # error'd out..print the message
        print("ERROR: " + error_message)
        # then return it
        return error_message

    # @desc Called internally during every tick of the state machine
    def _run(self, event):
        # call the current state's handler function and save it's returned data
        state_return = state_handler(event, localStorage)
        return state_return

    def _appendToDictByName():
        

