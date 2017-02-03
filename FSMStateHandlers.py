##########################################################################################
# FSM state functions
# @desc Definitions for each state of the FSM. They must return a state name
#       corresponding to the next state. Python doesn't have switch statements,
#       so using a lookup table to call the handler associated with each state.
##########################################################################################
def startupState(event):
    print("FSM: STARTUP_STATE[{0}]".format(event.name))
    if (event.name == "INIT"):
        return { "next_state": "TMP", "did_error": False }
    elif (event.name == "ENTRY"):
        return { "did_error": False }
    elif (event.name == "EXIT"):
        return { "did_error": False }
    else:
        print("ERROR: event has no event handler")

def tempState(event):
    print("FSM: TMP_STATE[{0},{1}]".format(event.name, str(event.data)))
    if (event.name == "TIMER"):
        return { "next_state": "TMP", "did_error": False}
    elif (event.name == "CARD_READ"):
        # print("FSM: TMP_STATE[{0},{1}]".format(event.name, event.data["id"]))
        return { "next_state": "TMP", "did_error": False }
    elif (event.name == "ENTRY"):
        return { "did_error": False }
    elif (event.name == "EXIT"):
        return { "did_error": False }
    else:
        return {"did_error": True, "error_message": "Event has no event handler in tempState"}
