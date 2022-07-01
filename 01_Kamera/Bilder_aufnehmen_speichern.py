import time
import os
import cv2 as cv
import RPi.GPIO as GPIO
import time
from V4l2_Functions import *

#Pin Definitions
Digital_Out_0 = 43 # Digital_Out_0
Digital_Out_1 = 44 # Digital_Out_1

GPIO.setmode(GPIO.BCM)  # BCM pin-numbering scheme from Raspberry Pi

GPIO.setup(Digital_Out_0, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Digital_Out_1, GPIO.OUT, initial=GPIO.LOW)


if __name__ == "__main__":

    counter = 0
    number_pallets_old = ""
    user = input("Start Pipeline ? Type (y/n)")
    if user == "y":
        print("y")

        set_camera_properties_left()    # Sets Camera Settings Left
        set_camera_properties_right()   # Sets Camera Settings Right
        video_capture_left, video_capture_right = Init_Pipeline()   # Starts both pipelines
        

        while(1):
            time.sleep(1)
            user = input("Number of Paletts? Type (0/1/2/3/4)")
            if user == "0":
                os.chdir('/home/nvidia/Palletfinder/02_Kamera/Images/0_Palette')
                number_pallets = "0_Palette_"
            elif user == "1":
                os.chdir('/home/nvidia/Palletfinder/02_Kamera/Images/1_Palette')
                number_pallets = "1_Palette_"
            elif user == "2":
                os.chdir('/home/nvidia/Palletfinder/02_Kamera/Images/2_Palette')
                number_pallets = "2_Palette_"
            elif user == "3":
                os.chdir('/home/nvidia/Palletfinder/02_Kamera/Images/3_Palette')
                number_pallets = "3_Palette_"
            elif user == "4":
                os.chdir('/home/nvidia/Palletfinder/02_Kamera/Images/4_Palette')
                number_pallets = "4_Palette_"

            if number_pallets == number_pallets_old:
                print("Counter keeps going")
            else :
                print("Counter reset")
                counter = 0
            user = input("Snap Picture? Type (y/n)")
            if user == "y":
                GPIO.output(Digital_Out_0, GPIO.HIGH)
                GPIO.output(Digital_Out_1, GPIO.HIGH)
                print("y")

                image = read_frame(video_capture_right)
                filename = str(number_pallets)+str(counter) + '.jpg' 
                cv.imwrite(filename, image)
                counter = counter+1

                image = read_frame(video_capture_left)
                filename = str(number_pallets)+str(counter) + '.jpg' 
                cv.imwrite(filename, image)
                counter = counter+1                        
                GPIO.output(Digital_Out_0, GPIO.LOW)
                GPIO.output(Digital_Out_1, GPIO.LOW) 
            user = input("Add Pictures? Type (y/n)")
            if user == "n":
                exit()
            else:
                number_pallets_old = number_pallets
    else :
        print("n\n","Pipeline not Startet!")

   
                




