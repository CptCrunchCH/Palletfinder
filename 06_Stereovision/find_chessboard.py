import sys
import glob
import cv2 as cv

chessboardSize = (9,6)
if __name__ == '__main__':
    imagesLeft = glob.glob('/home/nvidia/Palletfinder/06_Stereovision/images/imageL4.png')
    imagesRight = glob.glob('/home/nvidia/Palletfinder/06_Stereovision/images/frameR0.png')

    imgL = cv.imread(imagesLeft[0])
    grayL = cv.cvtColor(imgL, cv.COLOR_BGR2GRAY)
    cv.imshow("Grayimage",grayL)
    cv.waitKey(0)
    retL, cornersL = cv.findChessboardCorners(grayL, chessboardSize, None)
    print("retL = ",retL)
    print("cornersL = ", cornersL)

    