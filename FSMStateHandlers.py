from abc import abstractmethod, abstractproperty

##########################################################################################
# FSM state functions
# @desc Definitions for each state of the FSM. They must return a state name
#       corresponding to the next state. Python doesn't have switch statements,
#       so using a lookup table to call the handler associated with each state.
##########################################################################################
class InitState():
    def __init__(self):
        print "Initing StartupState"

    @abstractproperty
    def args(self):
        return [ "LocalStorage", "DropboxStorage"]

    @abstractmethod
    def run(self, args):
        print("FSM: TMP_STATE[{0},{1}]".format(args["event"].name, str(args["event"].data)))
        if (args["event"].name == "INIT"):
            return { "next_state": "TMP", "did_error": False }
        elif (args["event"].name == "ENTRY"):
            return { "did_error": False }
        elif (args["event"].name == "EXIT"):
            return { "did_error": False }
        else:
            print("ERROR: args[event] has no args[event] handler")
#
# def startupState(event, localStorage):
#     print("FSM: TMP_STATE[{0},{1}]".format(event.name, str(event.data)))
#     if (event.name == "INIT"):
#         return { "next_state": "TMP", "did_error": False }
#     elif (event.name == "ENTRY"):
#         return { "did_error": False }
#     elif (event.name == "EXIT"):
#         return { "did_error": False }
#     else:
#         print("ERROR: event has no event handler")

# def tempState(event, localStorage):
#     print("FSM: TMP_STATE[{0},{1}]".format(event.name, str(event.data)))
#     if (event.name == "TIMER"):
#         return { "next_state": "TMP", "did_error": False}
#     elif (event.name == "CARD_READ"):
#         # asyncronously write entry to the USB stick
#         Jobs.queue(Jobs.AsyncWriteTimeEntry(event.data, localStorage))
#         # print("FSM: TMP_STATE[{0},{1}]".format(event.name, event.data["id"]))
#         return { "next_state": "TMP", "did_error": False }
#     elif (event.name == "ENTRY"):
#         return { "did_error": False }
#     elif (event.name == "EXIT"):
#         return { "did_error": False }
#     else:
#         return {"did_error": True, "error_message": "Event has no event handler in tempState"}
