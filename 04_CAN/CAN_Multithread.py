#Python multithreading example to print current date.
#1. Define a subclass using threading.Thread class.
#2. Instantiate the subclass and trigger the thread.

from distutils.archive_util import make_archive
from multiprocessing.connection import wait
import threading
from socket import timeout
import can
from threading import Thread
from can.interface import Bus
import time
from os.path import exists
import os

from matplotlib import image
from V4l2_Functions import *
import RPi.GPIO as GPIO

class Docker_Thread (threading.Thread):
    def __init__(self,name):
        threading.Thread.__init__(self)
        self.name = name
    def run(self):
        print("\nStarting " + self.name)
        # Can Settings
        os.system("sudo docker stop Palletfinder")
        os.system("sudo docker rm Palletfinder")
        os.system("sudo docker run --restart=always --runtime nvidia -itd --name=Palletfinder --volume ~/Palletfinder:/home/Palletfinder nvcr.io/nvidia/l4t-ml:r32.6.1-py3")
        os.system("sudo docker exec Palletfinder /bin/bash -c 'pip3 install imutils'")
        os.system("sudo docker exec Palletfinder /bin/bash -c 'chmod 777 /home/Palletfinder/03_Make_Prediction/Makeprediction.py'")
        os.system("sudo docker exec Palletfinder /bin/bash -c 'chmod +x /home/Palletfinder/03_Make_Prediction/Makeprediction.py'")
        os.system("sudo docker exec Palletfinder /bin/bash -c '/usr/bin/python3.6 /home/Palletfinder/03_Make_Prediction/Prediction_V2.py' > /dev/null 2>&1 &")
        time.sleep(0.001)
        print("Exiting " + self.name)

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
        error = 0x00
    except:
        error = 0x01

    return error

def predict():
    try:
        file = open("03_Make_Prediction/output/Start_Prediction.txt","w")   # Start Prediction
        print("File Createt")
        while exists("03_Make_Prediction/output/prediction.txt"):  # Waiting for Prediction to end
            time.sleep(10)
        File = open("03_Make_Prediction/output/Prediction.txt","r")
        Prediction = File.read()
        if Prediction == "0_Palette":
            num_paletts = 0
        elif Prediction == "1_Palette":
            num_paletts = 1
        elif Prediction == "2_Palette":
            num_paletts = 2
        elif Prediction == "3_Palette":
            num_paletts = 3
        elif Prediction == "4_Palette":
            num_paletts = 4
            
        print(Prediction)
        error = 0x00
        status_predict = 0x01
    except:
        error = 0x02
        status_predict = 0x00
    return error, num_paletts, status_predict



def detect_height(num_pallets):
    try:
        height_per_pallet = 144 #mm
        h2 = 44 #mm
        h1 = num_pallets * height_per_pallet - h2
        error = 0
    except:
        error = 0x04
    return error, h1, h2

def create_can_message(status_predict,num_paletts,h1,h2):
    try:
        Data0 = status_predict
        #Höhe Boden bis Oberkannt Palette
        if (h1+h2 <= 255):
            Data4 = h1+h2
            Data5 = 0
        elif (h1+h2):
            Data4 = 255
            Data5 = h1+h2-255
        msg = can.Message(
        arbitration_id=0x1A7, data=[Data0, 1, 2, num_paletts, Data4, Data5, 6,7], is_extended_id=False
        )
        error = 0
    except:
        error = 0x08

    return error, msg

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
    thread2 = Docker_Thread("Thread 1: Starting Docker")
    thread2.start()

    # Can Settings
    send_filters = [
        {"can_id": 0x1A7, "can_mask": 0x7FF, "extended": False},
    ]
    bus_send = can.interface.Bus(channel="can0", bustype="socketcan", can_filters=send_filters)

    print("\nStarting Mainloop")
    while(1):
        if (thread1.msg_data == 1) or (thread1.msg_data == 2):

            error_snap_images = snap_images(path_left, path_right)          # Snap Images and save
            error_prediction, num_paletts, status_predict = predict()
            error_height, h1, h2 = detect_height(num_paletts)
            error_can_send, msg = create_can_message(status_predict,num_paletts,h1,h2)
            
            bus_send.send(msg)                                              
            thread1.msg_data = 0
        time.sleep(0.025)
            
            
            
      
        


