import cv2
from V4l2_Functions import *
import RPi.GPIO as GPIO
num = 0
set_camera_properties_left()
set_camera_properties_right()
video_capture_left, video_capture_right = Init_Pipeline()
#show_both_cameras(video_capture_left, video_capture_right)
#show_camera_left(video_capture_left)
#show_camera_Right(video_capture_right)

path_right = "/home/nvidia/Palletfinder/06_Stereovision/images/frameR"
path_left = "/home/nvidia/Palletfinder/06_Stereovision/images/imageL"

while (1):
    image_right = read_frame(video_capture_right)
    image_left = read_frame(video_capture_left)

    k = cv2.waitKey(5)

    if k == 27:
        breaks
    elif k == ord('s'): # wait for 's' key to save and exit
        cv2.imwrite(path_left + str(num) + ".png", image_left)
        cv2.imwrite(path_right+ str(num) + ".png", image_right)
        print("images saved!")
        num += 1
        
    cv2.imshow('Img 1',image_left)
    cv2.imshow('Img 2',image_right)