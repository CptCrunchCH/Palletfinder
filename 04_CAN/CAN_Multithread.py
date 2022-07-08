#Python multithreading example to print current date.
#1. Define a subclass using threading.Thread class.
#2. Instantiate the subclass and trigger the thread.

from multiprocessing.connection import wait
import threading
from socket import timeout
import can
from threading import Thread
from can.interface import Bus
import time

from matplotlib import image
from V4l2_Functions import *
import RPi.GPIO as GPIO

def can_send_mesage(bus,msg):
    bus.send(msg)

class can_receive_thread (threading.Thread):
    def __init__(self,name,msg,msg_data):
        threading.Thread.__init__(self)
        self.name = name
        self.msg = msg
        self.msg_data = msg_data

    def run(self):
        print("\nStarting " + self.name)
        # Can Settings
        filters = [
            {"can_id": 0x230, "can_mask": 0x7FF, "extended": False},
        ]
        bus_receive = can.interface.Bus(channel="can0", bustype="socketcan", can_filters=filters)
        
        msg_old = 10
        while(1):
            self.msg = bus_receive.recv()
            self.msg_data = self.msg.data[0]
            time.sleep(0.001)
            if self.msg.data[0] != msg_old:
                if self.msg.data[0] == 1:
                    state = "Start aufnehmen"
                    print(state)
                elif self.msg.data[0] == 2:
                    state = "Start abgeben"
                    print(state)
                elif self.msg.data[0] == 4:
                    state = "Error"
                    print(state)
                elif self.msg.data[0] == 8:
                    state = "Reset"
                    print(state)
            msg_old = self.msg.data[0]

        print("Exiting " + self.name)


if __name__ == "__main__":
    # Start new Threads    
    thread1 = can_receive_thread("Thread 1: Reading CAN",0,0)
    thread1.start()

    # Can Settings
    send_filters = [
        {"can_id": 0x1A7, "can_mask": 0x7FF, "extended": False},
    ]
    bus_send = can.interface.Bus(channel="can0", bustype="socketcan", can_filters=send_filters)
    msg = can.Message(
        arbitration_id=0x1A7, data=[1, 2, 3, 4, 5, 6], is_extended_id=False
        )

    print("\nStarting Mainloop")
    while(1):
        if thread1.msg_data == 1:
            can_send_mesage(bus_send,msg)
            thread1.msg_data = 0
        time.sleep(0.025)
            
            
            
      
        


