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
import cv2 as cv

from V4l2_Functions import *

from matplotlib import image
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
        print("\n[Info] Please Wait 20s")
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

def snap_images(capL, capR):
    try: 
        start_time = time.time()
        path_right = "03_Make_Prediction/Images/frame_right.png"
        path_left = "03_Make_Prediction/Images/frame_left.png"
        GPIO.output(Digital_Out_0, GPIO.HIGH)
        GPIO.output(Digital_Out_1, GPIO.HIGH)

        ret, image_left = capL.read()
        ret, image_right = capR.read()
        
        GPIO.output(Digital_Out_0, GPIO.LOW)
        GPIO.output(Digital_Out_1, GPIO.LOW) 

        cv.imwrite(path_left, image_left)
        cv.imwrite(path_right, image_right)
    
        print("It took {} to snap picture".format(time.time() - start_time))
        error = 0x00
    except:
        error = 0x01

    return error

def predict():
    
    file = open("/home/nvidia/Palletfinder/03_Make_Prediction/output/Start_Prediction.txt","w")   # Start Prediction
    print("File Createt")
    while not(exists("/home/nvidia/Palletfinder/03_Make_Prediction/output/Predictions/endY_right.txt")):
        time.sleep(1)            
    start_time = time.time()
    # Reading Number Pallets for both images
    File = open("/home/nvidia/Palletfinder/03_Make_Prediction/output/Predictions/Label_left.txt","r")
    num_palletsL = File.read()
    os.remove("/home/nvidia/Palletfinder/03_Make_Prediction/output/Predictions/Label_left.txt")
    File = open("/home/nvidia/Palletfinder/03_Make_Prediction/output/Predictions/Label_right.txt","r")
    num_palletsR = File.read()
    os.remove("/home/nvidia/Palletfinder/03_Make_Prediction/output/Predictions/Label_right.txt")

    # Reading endx Value
    File = open("/home/nvidia/Palletfinder/03_Make_Prediction/output/Predictions/endX_left.txt","r")
    endX_left = File.read()
    os.remove("/home/nvidia/Palletfinder/03_Make_Prediction/output/Predictions/endX_left.txt")
    File = open("/home/nvidia/Palletfinder/03_Make_Prediction/output/Predictions/endX_right.txt","r")
    endX_right = File.read()
    os.remove("/home/nvidia/Palletfinder/03_Make_Prediction/output/Predictions/endX_right.txt")
    
    # Reading endy Value
    File = open("/home/nvidia/Palletfinder/03_Make_Prediction/output/Predictions/endY_left.txt","r")
    endY_left = File.read()
    os.remove("/home/nvidia/Palletfinder/03_Make_Prediction/output/Predictions/endY_left.txt")
    File = open("/home/nvidia/Palletfinder/03_Make_Prediction/output/Predictions/endY_right.txt","r")
    endY_right = File.read()
    os.remove("/home/nvidia/Palletfinder/03_Make_Prediction/output/Predictions/endY_right.txt")
    
    # Reading startx Value
    File = open("/home/nvidia/Palletfinder/03_Make_Prediction/output/Predictions/startX_left.txt","r")
    startX_left = File.read()
    os.remove("/home/nvidia/Palletfinder/03_Make_Prediction/output/Predictions/startX_left.txt")
    File = open("/home/nvidia/Palletfinder/03_Make_Prediction/output/Predictions/startX_right.txt","r")
    startX_right = File.read()
    os.remove("/home/nvidia/Palletfinder/03_Make_Prediction/output/Predictions/startX_right.txt")
    
    # Reading startY Value
    File = open("/home/nvidia/Palletfinder/03_Make_Prediction/output/Predictions/startY_left.txt","r")
    startY_left = File.read()
    os.remove("/home/nvidia/Palletfinder/03_Make_Prediction/output/Predictions/startY_left.txt")
    File = open("/home/nvidia/Palletfinder/03_Make_Prediction/output/Predictions/startY_right.txt","r")
    startY_right = File.read()
    os.remove("/home/nvidia/Palletfinder/03_Make_Prediction/output/Predictions/startY_right.txt")

    bboxL = [int(startX_left),int(startY_left),int(endX_left),int(endY_left)]
    bboxR = [int(startX_right),int(startY_right),int(endX_right),int(endY_right)]

    num_palletsR = num_palletsR.replace('"','')
    num_palletsL = num_palletsL.replace('"','')
    
    print("It took {} to predict".format(time.time() - start_time))
    
    error = 0x00
    status_predict = 0x01
    return int(num_palletsL), int(num_palletsR), bboxL, bboxR, status_predict, error
   
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

def initcam():
    cap0 = cv2.VideoCapture(0)
    cap1 = cv2.VideoCapture(1)
    if not (cap0.isOpened()):
        print("Could not open video device0")
    if not (cap1.isOpened()):
        print("Could not open video device1")
    cap0.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap0.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cap0.set(cv2.CAP_PROP_FPS, 30.0)
    cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cap1.set(cv2.CAP_PROP_FPS, 30.0)

    return cap0, cap1

if __name__ == '__main__':
    capL, capR = initcam()

    Digital_Out_0 = 43 # Digital_Out_0
    Digital_Out_1 = 44 # Digital_Out_1

    GPIO.setmode(GPIO.BCM)  # BCM pin-numbering scheme from Raspberry Pi

    GPIO.setup(Digital_Out_0, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(Digital_Out_1, GPIO.OUT, initial=GPIO.LOW)

    # Start new Threads    
    thread1 = can_receive_thread("Thread 1: Reading CAN",0,0)
    thread1.start()
    thread2 = Docker_Thread("Thread 2: Starting Docker")
    thread2.start()

    # Can Settings
    send_filters = [
        {"can_id": 0x1A7, "can_mask": 0x7FF, "extended": False},
    ]
    bus_send = can.interface.Bus(channel="can0", bustype="socketcan", can_filters=send_filters)
    print("\nStarting Mainloop")
    while(1):
        if (thread1.msg_data == 1) or (thread1.msg_data == 2):

            error_snap_images = snap_images(capL, capR)          # Snap Images and save
            num_palletsL, num_palletsR, bboxL, bboxR, status_predict, error = predict()

            if num_palletsL == num_palletsR:
                num_pallets = num_palletsL
                print("Predicted Number of Pallets are the same")
            else:
                error = 1
                print("[Error] Predicted Number of Pallets are not the same !")



            # error_height, h1, h2 = detect_height(num_pallets)
            # error_can_send, msg = create_can_message(status_predict,num_pallets,h1,h2)
            
            # bus_send.send(msg)                                              
            thread1.msg_data = 0
        time.sleep(0.025)

capL.release()
capR.release()