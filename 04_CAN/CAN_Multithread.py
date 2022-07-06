#Python multithreading example to print current date.
#1. Define a subclass using threading.Thread class.
#2. Instantiate the subclass and trigger the thread.

import threading
from socket import timeout
import can
from threading import Thread
from can.interface import Bus
import time

from matplotlib import image
from V4l2_Functions import *
import RPi.GPIO as GPIO

#Pin Definitions
Digital_Out_0 = 43 # Digital_Out_0
Digital_Out_1 = 44 # Digital_Out_1

GPIO.setmode(GPIO.BCM)  # BCM pin-numbering scheme from Raspberry Pi

GPIO.setup(Digital_Out_0, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Digital_Out_1, GPIO.OUT, initial=GPIO.LOW)

class can_sending_thread (threading.Thread):
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
        while(1):
            msg = can.Message(
            arbitration_id=0x189, data=[1, 2, 3, 4, 5, 6], is_extended_id=False
            )
            bus.send(msg)
            time.sleep(2)
        print("Exiting " + self.name)

class can_receive_thread (threading.Thread):
    def __init__(self,name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        print("\nStarting " + self.name)
        # Can Settings
        filters = [
            {"can_id": 0x209, "can_mask": 0x7FF, "extended": False},
        ]
        bus = can.interface.Bus(channel="can0", bustype="socketcan", can_filters=filters)
        
        msg_old = 10

        while(1):
            msg = bus.recv()
            if msg.data[0] != msg_old:
                if msg.data[0] == 0:
                    print("Stop")
                elif msg.data[0] == 1:
                    print("Start")
                elif msg.data[0] == 2:
                    print("Error")
            msg_old = msg.data[0]
        print("Exiting " + self.name)

def snap_image ():
    path_right = "04_CAN/Images/frame_right.png"
    path_left = "04_CAN/Images/frame_left.png"
    start_time = time.time()
    set_camera_properties_left()
    set_camera_properties_right()
    video_capture_left, video_capture_right = Init_Pipeline()
    GPIO.output(Digital_Out_0, GPIO.HIGH)
    GPIO.output(Digital_Out_1, GPIO.HIGH)
    image_right = read_frame(video_capture_right)
    image_left = read_frame(video_capture_left)

    GPIO.output(Digital_Out_0, GPIO.LOW)
    GPIO.output(Digital_Out_1, GPIO.LOW) 

    cv2.imwrite(path_left, image_left)
    cv2.imwrite(path_right, image_right)
    print("It took {} to snap picture".format(time.time() - start_time))


# Create new threads


if __name__ == "__main__":
    # Start new Threads    
    print("\nStarting Mainloop")
    thread0 = can_sending_thread("Thread 1: Sending CAN",0)
    thread1 = can_receive_thread("Thread 2: Reading CAN")
    thread0.start()
    thread1.start()

            
            
            
      
        


