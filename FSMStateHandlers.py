##########################################################################################
# FSM state functions
# @desc Definitions for each state of the FSM. They must return a state name
#       corresponding to the next state. Python doesn't have switch statements,
#       so using a lookup table to call the handler associated with each state.
##########################################################################################
def startupState(event):
    print("FSM: Entered STARTUP state")
    return { "next_state": "TMP", "did_error": False }

def tempState(event):
    print("FSM: Entered TMP state")
    return { "next_state": "TMP", "did_error": True, "error_message": "Exited temp state"}
