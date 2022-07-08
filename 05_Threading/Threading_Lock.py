# A lock can be used to protect one or multiple shared variables and they may be
# variables of any type. The shared variables will be protected from race conditions
# as long as all access and changes to the variables are protected by the lock

# Each thread interested in the variable must first acquire the lock, and then release
# it once they are finished with the variable. This will ensure that only one thread
# can access the variable at a time. A thread trying to acquire the lock that has already
# been acquired must wait until the lock has been released again.

import threading

# create a shared lock
lock = threading.Lock()
...
# acquire the lock
lock.acquire()
# read or write the shared variable
...
# release the lock
lock.release()

# SuperFastPython.com
# example of a mutual exclusion (mutex) lock
from time import sleep
from random import random
from threading import Thread
from threading import Lock
 
# work function
def task(lock, identifier, value):
    # acquire the lock
    with lock:
        print(f'>thread {identifier} got the lock, sleeping for {value}')
        sleep(value)
 
# create a shared lock
lock = Lock()
# start a few threads that attempt to execute the same critical section
for i in range(10):
    # start a thread
    Thread(target=task, args=(lock, i, random())).start()
# wait for all threads to finish...