import numpy as np
import cv2
import subprocess

#------------Init_Pipeline------------#
# Defnies and initializes both pipelines for video0 and video1
def Init_Pipeline():
    # ASSIGN CAMERA ADRESS to DEVICE HERE!
    pipeline_Left = " ! ".join(["v4l2src device=/dev/video0",
                        "video/x-raw, width=1280, height=720, framerate=30/1",
                        "videoconvert",
                        "video/x-raw, format=GRAY8",
                        "appsink"
                        ])

    pipeline_Right = " ! ".join(["v4l2src device=/dev/video1",
                        "video/x-raw, width=1280, height=720, framerate=30/1",
                        "videoconvert",
                        "video/x-raw, format=GRAY8",
                        "appsink"
                        ])
    video_capture_Left = cv2.VideoCapture(pipeline_Left, cv2.CAP_GSTREAMER)
    video_capture_Right = cv2.VideoCapture(pipeline_Right, cv2.CAP_GSTREAMER)
    return video_capture_Left, video_capture_Right


#------------set_camera_properties_right------------#
# Sets the camera settings for the right camera (video1)
def set_camera_properties_right():
    cam_props_right = {'brightness': 500, 'gain': 0, 'exposure_absolute': 3333,
             'exposure_time_us': 33333, 'gain_db_100': 0, 'trigger_mode': 0,
             'trigger_delay': 0, 'strobe_enable': 0,
             'strobe_polarity': 0, 'strobe_exposure': 0, 'strobe_duration': 100,
             'strobe_delay': 0, 'gpout': 0,'gpin': 0,'trigger_polarity': 0,
             'flip_horizontal': 1, 'flip_vertical': 1}
    for key in cam_props_right:
        subprocess.call(['v4l2-ctl -d /dev/video1 -c {}={}'.format(key, str(cam_props_right[key]))],
                    shell=True)


#------------set_camera_properties_left------------#
# Sets the camera settings for the left camera (video1)
def set_camera_properties_left():
    cam_props_left = {'brightness': 500, 'gain': 0, 'exposure_absolute': 3333,
             'exposure_time_us': 33333, 'gain_db_100': 0, 'trigger_mode': 0,
             'trigger_delay': 0, 'strobe_enable': 0,
             'strobe_polarity': 0, 'strobe_exposure': 0, 'strobe_duration': 100,
             'strobe_delay': 0, 'gpout': 0,'gpin': 0,'trigger_polarity': 0,
             'flip_horizontal': 0, 'flip_vertical': 0}
    for key in cam_props_left:
        subprocess.call(['v4l2-ctl -d /dev/video0 -c {}={}'.format(key, str(cam_props_left[key]))],
                    shell=True)

#------------read frame------------#
# Reads a frame from the given Pipeline
def read_frame(video_capture):
    if video_capture.isOpened():
        ret_val, frame = video_capture.read()
    return ret_val, frame


   
  
# Importing Image module from PIL package 
from PIL import Image

if __name__ == "__main__":
    set_camera_properties_left()
    set_camera_properties_right()
    video_capture_left, video_capture_right = Init_Pipeline()
    #show_both_cameras(video_capture_left, video_capture_right)
    #show_camera_left(video_capture_left)
    # show_camera_Right(video_capture_right)

    path_right = "05_Make_Prediction/Images/frame_right.png"
    path_left = "05_Make_Prediction/Images/frame_left.png"
    ret_val, image_right = read_frame(video_capture_right)
    ret_val, image_left = read_frame(video_capture_left)

    cv2.imwrite(path_left, image_left)
    cv2.imwrite(path_right, image_right)