from V4l2_Functions import *
import RPi.GPIO as GPIO

#Pin Definitions
Digital_Out_0 = 43 # Digital_Out_0
Digital_Out_1 = 44 # Digital_Out_1

GPIO.setmode(GPIO.BCM)  # BCM pin-numbering scheme from Raspberry Pi

GPIO.setup(Digital_Out_0, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Digital_Out_1, GPIO.OUT, initial=GPIO.LOW)

if __name__ == "__main__":
    set_camera_properties_left()
    set_camera_properties_right()
    video_capture_left, video_capture_right = Init_Pipeline()
    #show_both_cameras(video_capture_left, video_capture_right)
    #show_camera_left(video_capture_left)
    # show_camera_Right(video_capture_right)

    path_right = "03_Make_Prediction/Images/frame_right.png"
    path_left = "03_Make_Prediction/Images/frame_left.png"
    GPIO.output(Digital_Out_0, GPIO.HIGH)
    GPIO.output(Digital_Out_1, GPIO.HIGH)
    image_right = read_frame(video_capture_right)
    image_left = read_frame(video_capture_left)

    cv2.imwrite(path_left, image_left)
    cv2.imwrite(path_right, image_right)
    
    GPIO.output(Digital_Out_0, GPIO.LOW)
    GPIO.output(Digital_Out_1, GPIO.LOW) 