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
            time.sleep(0.001)
            if self.msg.data[0] != msg_old:
                if self.msg.data[0] == 1:
                    state = "Start aufnehmen"
                    self.msg_data = self.msg.data[0]
                    print(state)
                elif self.msg.data[0] == 2:
                    state = "Start abgeben"
                    self.msg_data = self.msg.data[0]
                    print(state)
                elif self.msg.data[0] == 4:
                    state = "Error"
                    self.msg_data = self.msg.data[0]
                    print(state)
                elif self.msg.data[0] == 8:
                    state = "Reset"
                    self.msg_data = self.msg.data[0]
                    print(state)
            msg_old = self.msg.data[0]
        time.sleep(0.001)
        print("Exiting " + self.name)

def snap_images(path_left, path_right):
    try: 
        start_time = time.time()
        GPIO.output(Digital_Out_0, GPIO.HIGH)
        GPIO.output(Digital_Out_1, GPIO.HIGH)
        image_right = read_frame(video_capture_right)
        image_left = read_frame(video_capture_left)

        cv2.imwrite(path_left, image_left)
        cv2.imwrite(path_right, image_right)
        
        GPIO.output(Digital_Out_0, GPIO.LOW)
        GPIO.output(Digital_Out_1, GPIO.LOW) 
        print("It took {} to snap picture".format(time.time() - start_time))
        error = 0
    except:
        error = 1

    return error



if __name__ == '__main__':
    Digital_Out_0 = 43 # Digital_Out_0
    Digital_Out_1 = 44 # Digital_Out_1

    GPIO.setmode(GPIO.BCM)  # BCM pin-numbering scheme from Raspberry Pi

    GPIO.setup(Digital_Out_0, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(Digital_Out_1, GPIO.OUT, initial=GPIO.LOW)

    set_camera_properties_left()
    set_camera_properties_right()
    video_capture_left, video_capture_right = Init_Pipeline()
    
    path_right = "03_Make_Prediction/Images/frame_right.png"
    path_left = "03_Make_Prediction/Images/frame_left.png"

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
        if (thread1.msg_data == 1) or (thread1.msg_data == 2):

            error = snap_images(path_left, path_right)

            Error = True          

            bus_send.send(msg)
            thread1.msg_data = 0
        time.sleep(0.025)
            
            
            
      
        


