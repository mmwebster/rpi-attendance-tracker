#/usr/bin/env python

#################################################################################
# Import libraries
#################################################################################
import evdev # lib for keyboard input event detection

#################################################################################
# Perform initializations
#################################################################################

#################################################################################
# Main logic
#################################################################################
# scan for devices
devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
# find card reader device
if (len(devices) > 0):
    print("Input event devices available ("
            + str(len(devices)) + "). Devices are: ")
    # init card reader discovery bool
    discovered_card_reader = False
    # display input devices
    for i, device in enumerate(devices):
        print("    " + str(i) + ") (" + device.fn + ", "
                + device.name + ", " + device.phys + ")")
        # search for card reader by its name, "HID c216:0180"
        # if str(device.name) == "Mitsumi Electric Apple Extended USB Keyboard":
        if str(device.name) == "HID c216:0180":
            print("Discovered card reader..listening for events \
                    until test harness is closed.")
            # rename device for readability
            card_reader = device
            # indefinitely listen for events
            for event in card_reader.read_loop():
                if event.type == evdev.ecodes.EV_KEY:
                    print(str(event))

    # error out if unable to find card reader
    if not discovered_card_reader:
        print("ERROR: Unable to find the card reader")
else:
    print("ERROR: No input event devices available")

#################################################################################
# House keeping..close interfaces and processes
#################################################################################
