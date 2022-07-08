# Shares a boolean variable between threads

import threading
from threading import Thread


# The event class will protect a boolean variable ensuring all access and change 
# to the variable is thread safe, avoiding race conditions.
event = threading.Event()

# it can be shared between threads

# The status of the event can be checked safely via the is_set() function

if event.is_set():
    x = 0

# The value event can be changed by multiple different threads. 
# It can be set to True via the set() function and set False via the clear() function.

# set the event true
event.set()
# ...
# set the event false
event.clear()

# SuperFastPython.com
# example of using an event object
from time import sleep
from random import random
from threading import Thread
from threading import Event
 
# target task function
def task(event, number):
    # wait for the event to be set
    event.wait()
    # begin processing
    value = random()
    sleep(value)
    print(f'Thread {number} got {value}')
 
# create a shared event object
event = Event()
# create a suite of threads
for i in range(5):
    thread = Thread(target=task, args=(event, i))
    thread.start()
# block for a moment
print('Main thread blocking...')
sleep(2)
# start processing in all threads
event.set()
# wait for all the threads to finish...