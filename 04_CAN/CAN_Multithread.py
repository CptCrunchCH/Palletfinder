#Python multithreading example to print current date.
#1. Define a subclass using threading.Thread class.
#2. Instantiate the subclass and trigger the thread.

import threading
from multiprocessing.connection import Listener
from socket import timeout
import can
from threading import Thread



class can_receive_thread (threading.Thread):
    def __init__(self,name, msg):
        threading.Thread.__init__(self)
        self.name = name
        self.msg = msg
    def run(self):
        print("\nStarting " + self.name)
        can.rc['interface'] = 'socketcan'
        can.rc['channel'] = 'can0'
        can.rc['bitrate'] = 250000
        bus = Bus()
        msg_old = 0
        while(1):
            self.msg = bus.recv()
            msgdata = self.msg.data[0]
            if msgdata != msg_old:
                if self.msg.data[0] == 0:
                    print("Stop")
                elif self.msg.data[0] == 1:
                    print("Start")
                elif self.msg.data[0] == 2:
                    print("FYI")
                print(self.msg)
            msg_old = self.msg.data[0]
                

        print("Exiting " + self.name)

# Create new threads
thread1 = can_receive_thread("Thread 1",0)

# Start new Threads
thread1.start()
thread1.join()

msg = thread1.msg



