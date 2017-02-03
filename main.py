#!/usr/bin/env python

#####################################################################################
# Import libraries
#####################################################################################
import threading
import EventListeners # contains all event listeners
import FSMStateHandlers # contains all state handlers
from Event import Event
from Queue import PriorityQueue

#####################################################################################
# Globals
#####################################################################################


#####################################################################################
# FSM body
#####################################################################################
def fsm_run(state_handler, event):
    # call the current state's handler function and save it's returned data
    state_return = state_handler(event)
    return state_return


#####################################################################################
# Main logic
#####################################################################################
def main():
    #################################################################################
    # Perform initializations
    #################################################################################
    # run all lib tests
    print("MAIN: Started up! Running tests.")
    # TODO: run tests here
    # TODO: check if each test passed and proceed if so

    # init and declare FSM properties
    state_handlers = {
            "STARTUP": FSMStateHandlers.startupState,
            "TMP": FSMStateHandlers.tempState
            }
    current_state_str = "STARTUP"
    # init the next_state reference with the startupState handler
    current_state_handler = state_handlers[current_state_str]
    did_error = False
    error_message = ""

    # instantiate the event queue
    eventQueue = PriorityQueue() # thread-safe queue
    # instantiate all event listeners
    eventListeners = [
            EventListeners.Init(eventQueue), # passes init event to FSM
            EventListeners.Timer(eventQueue, 5.0),
            EventListeners.CardReader(eventQueue, period, "my-device"),
            ]
    # startup all event listener threads
    for eventListener in eventListeners:
        eventListener.start()

    # Begin the main FSM runloop
    print("MAIN: Starting up the main FSM...")
    while not did_error:
        # If there are events to process
        if not eventQueue.empty():
            # Fetch the highest priority event and process it
            state_return = fsm_run(current_state_handler, eventQueue.get())
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
                fsm_run(current_state_handler, Event(Event.EVENTS["EXIT"]))
                # run next state with entry event (ignore return)
                fsm_run(next_state_handler, Event(Event.EVENTS["ENTRY"]))

            # set current state to next
            current_state_handler = next_state_handler
            current_state_str = next_state_str

    # error'd out..print the message
    print("ERROR: " + error_message)

main()

#####################################################################################
# House keeping..close interfaces and processes
#####################################################################################

# # clean up all libs on exit
# si7021.__exit__(None, None, None)
# seg7.__exit__(None, None, None)
# servo.__exit__(None, None, None)
# mailer.__exit__(None, None, None)
# # close pi gpio ref
# pi.stop()
