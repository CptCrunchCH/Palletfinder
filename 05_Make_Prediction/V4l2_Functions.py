##########################################################################
#   V4l2_Functions.py
##########################################################################
#   Author: F.Heimann
#   Date:   17.06.2022
#
#
#   Imports:
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
    return frame


#------------show_camera_left------------#
# Shows the left camera with openCV
def show_camera_left(video_capture_left):
    video_capture_Left = video_capture_left
    window_Left = "USB Camera Left"
    window_handle_Left = cv2.namedWindow(
                window_Left, cv2.WINDOW_NORMAL)
    cv2.moveWindow(window_Left,50,100)
    while True:
        frame_Left = read_frame(video_capture_Left)
        cv2.imshow(window_Left, frame_Left)
        keyCode = cv2.waitKey(10) & 0xFF
        # Stop the program on the ESC key or 'q'
        if keyCode == 27 or keyCode == ord('q'):
            video_capture_Left.release()
            cv2.destroyAllWindows()
            break


#------------show_camera_right------------#
# Shows the Right camera with openCV
def show_camera_Right(video_capture_right):
    video_capture_Right=video_capture_right
    window_Right = "USB Camera Right"
    window_handle_Right = cv2.namedWindow(
                window_Right, cv2.WINDOW_NORMAL)
    cv2.moveWindow(window_Right,1000,100)
    while True:
        frame_Right = read_frame(video_capture_Right)
        cv2.imshow(window_Right, frame_Right)
        keyCode = cv2.waitKey(10) & 0xFF
        # Stop the program on the ESC key or 'q'
        if keyCode == 27 or keyCode == ord('q'):
            video_capture_Right.release()
            cv2.destroyAllWindows()
            break

#------------show_both_cameras-----------#
# Shows both cameras with openCV
def show_both_cameras(video_capture_left, video_capture_right):
    video_capture_Left = video_capture_left
    video_capture_Right = video_capture_right
    window_Left = "USB Camera Left"
    window_Right = "USB Camera Right"
    window_handle_Left = cv2.namedWindow(
                window_Left, cv2.WINDOW_NORMAL)
    cv2.moveWindow(window_Left,50,100)
    window_handle_Right = cv2.namedWindow(
                window_Right, cv2.WINDOW_NORMAL)
    cv2.moveWindow(window_Right,1000,100)
    while True:
        frame_Left = read_frame(video_capture_Left)
        frame_Right = read_frame(video_capture_Right)
        cv2.imshow(window_Left, frame_Left)
        cv2.imshow(window_Right, frame_Right)
        keyCode = cv2.waitKey(10) & 0xFF
        # Stop the program on the ESC key or 'q'
        if keyCode == 27 or keyCode == ord('q'):
            video_capture_Left.release()
            video_capture_Right.release()
            cv2.destroyAllWindows()
            break



