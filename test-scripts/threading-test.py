#/usr/bin/env python

#################################################################################
# Import libraries
#################################################################################
import threading
import time
try:
    import Queue as Q  # ver. < 3.0
except ImportError:
    import queue as Q

#################################################################################
# Perform initializations
#################################################################################

#################################################################################
# Main logic
#################################################################################
# def hello():
#     print("hello, world")
#
# t = threading.Timer(5.0, hello)
# t.start()  # after 30 seconds, "hello, world" will be printed
threads = []

class Event(object):
    def __init__(self, priority, value):
        self.priority = priority
        self.value = str(value)
    def __cmp__(self, other):
        return cmp(self.priority, other.priority)

eventQueue = Q.PriorityQueue() # thread safe

def worker(num):
    """thread worker function"""
    if num != 4:
        # wait until the last thread spun up
        while len(threads) < 5:
            time.sleep(.01)
        # join this thread with the last spun up thread to make it complete only
        # after the last thread completes
        threads[num + 1].join()
        # execute the thread
        # post an event of equal priority
        print("Worker " + str(num) + ". Active count is " + str(threading.active_count()))
        if num == 2:
            eventQueue.put(Event(1, num))
        else:
            eventQueue.put(Event(2, num))
        return
    else:
        # execute the thread
        print("Worker " + str(num) + ". Active count is " + str(threading.active_count()))
        eventQueue.put(Event(1, num))
        return

for i in range(5):
    t = threading.Thread(target=worker, args=(i,))
    threads.append(t)
    t.start()

while True:
    if not eventQueue.empty() and eventQueue.qsize() > 1:
        newEvent = eventQueue.get()
        print("Processing event (value={0}, priority={1})".format(newEvent.value, newEvent.priority))


#################################################################################
# House keeping..close interfaces and processes
#################################################################################
