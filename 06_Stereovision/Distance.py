import cv2 as cv
from Calibration import *
from triangulation import *
# Read Images from camera 

def get_bbox():
    File_endxL = open("/home/nvidia/Palletfinder/03_Make_Prediction/output/Predictions/endX_left.txt","r")   # Start Prediction
    endxL = File_endxL.read()
    File_endxR = open("/home/nvidia/Palletfinder/03_Make_Prediction/output/Predictions/endX_right.txt","r")   # Start Prediction
    endxR = File_endxR.read()
    File_endyL = open("/home/nvidia/Palletfinder/03_Make_Prediction/output/Predictions/endY_left.txt","r")   # Start Prediction
    endyL = File_endyL.read()
    File_endyR = open("/home/nvidia/Palletfinder/03_Make_Prediction/output/Predictions/endY_right.txt","r")   # Start Prediction
    endyR = File_endyR.read()
    File_startxL = open("/home/nvidia/Palletfinder/03_Make_Prediction/output/Predictions/startX_left.txt","r")   # Start Prediction
    startxL = File_startxL.read()
    File_startxR = open("/home/nvidia/Palletfinder/03_Make_Prediction/output/Predictions/startX_right.txt","r")   # Start Prediction
    startxR = File_startxR.read()
    File_startyL = open("/home/nvidia/Palletfinder/03_Make_Prediction/output/Predictions/startY_left.txt","r")   # Start Prediction
    startyL = File_startyL.read()
    File_startyR = open("/home/nvidia/Palletfinder/03_Make_Prediction/output/Predictions/startY_right.txt","r")   # Start Prediction
    startyR = File_startyR.read()
    bboxL = [int(startxL),int(startyL),int(endxL),int(endyL)]
    bboxR = [int(startxR),int(startyR),int(endxR),int(endyR)]
    return bboxL, bboxR


path_right = "/home/nvidia/Palletfinder/03_Make_Prediction/output/Predictions/right_prediction.png"
path_left = "/home/nvidia/Palletfinder/03_Make_Prediction/output/Predictions/left_prediction.png"

# Stereo vision setup parameters
frame_rate = 30    #Camera frame rate (maximum at 120 fps)
B = 12.5               #Distance between the cameras [cm]
f = 6              #Camera lense's focal length [mm]
alpha = 63.2        #Camera field of view in the horisontal plane [degrees]

if __name__ == '__main__':
    frame_right = cv.imread(path_right)
    frame_left = cv.imread(path_left)

    orig_left = frame_left.copy()
    orig_right = frame_right.copy()

    #frame_right, frame_left = undistortRectify(frame_right, frame_left)
    start = time.time()
            
    ################## CALCULATING DEPTH #########################################################

    center_right = 0
    center_left = 0

    bboxL, bboxR = get_bbox()
    print("bboxL", bboxL)
    print("bboxR", bboxR)

    center_pointL = bboxL[0], bboxL[1], (bboxL[2]-bboxL[0]), (bboxL[3]-bboxL[1])
    center_pointR = bboxR[0], bboxR[1], (bboxR[2]-bboxR[0]), (bboxR[3]-bboxR[1])
    print("center pointL", center_pointL)
    print("center pointR", center_pointR)

    depth = find_depth(center_pointR, center_pointL, frame_right, frame_left, B, f, alpha)
    depth = abs(depth)

    cv2.putText(frame_right, "Distance: " + str(round(depth,1))+ " [cm]", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0,0,255),2)
    cv2.putText(frame_left, "Distance: " + str(round(depth,1)) + " [cm]", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0,0,255),2)
    # Multiply computer value with 205.8 to get real-life depth in [cm]. The factor was found manually.
    print("Depth: ", str(round(depth,1)))

    # Show the frames
    cv2.imshow("frame right", frame_right) 
    cv2.imshow("frame left", frame_left)
    cv.waitKey(0)




    