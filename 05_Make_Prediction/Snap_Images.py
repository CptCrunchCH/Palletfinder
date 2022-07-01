from V4l2_Functions import *
if __name__ == "__main__":
    set_camera_properties_left()
    set_camera_properties_right()
    video_capture_left, video_capture_right = Init_Pipeline()
    #show_both_cameras(video_capture_left, video_capture_right)
    #show_camera_left(video_capture_left)
    # show_camera_Right(video_capture_right)

    path_right = "05_Make_Prediction/Images/frame_right.png"
    path_left = "05_Make_Prediction/Images/frame_left.png"
    image_right = read_frame(video_capture_right)
    image_left = read_frame(video_capture_left)

    cv2.imwrite(path_left, image_left)
    cv2.imwrite(path_right, image_right)