#/usr/bin/env python

#######################################################################
# Import libraries
#######################################################################
import evdev # lib for keyboard input event detection

#######################################################################
# Perform initializations
#######################################################################

#######################################################################
# Main logic
#######################################################################
# scan for devices
devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
# find card reader device
if (len(devices) > 0):
    print("Input event devices available. Devices are: ")
    for device, i in enumerate(devices):
        print("   ", i, ") ", device.fn, device.name, device.phys)
else:
    print("ERROR: No input event devices available")

#######################################################################
# House keeping..close interfaces and processes
#######################################################################
