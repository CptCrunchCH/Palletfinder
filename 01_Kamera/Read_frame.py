# app.py
import cv2

cap0 = cv2.VideoCapture(0)
cap1 = cv2.VideoCapture(1)

#Check if camera was opened correctly
if not (cap0.isOpened()):
    print("Could not open video device")


#Set the resolution
cap0.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap0.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap0.set(cv2.CAP_PROP_FPS, 30.0)
cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap1.set(cv2.CAP_PROP_FPS, 30.0)
# Capture frame-by-frame
while(True):
    ret, frameL = cap0.read()
    ret, frameR = cap1.read()

    # Display the resulting frame
    
    cv2.imshow("previewL",frameL)
    cv2.imshow("previewR",frameR)
    

    #Waits for a user input to quit the application
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap0.release()
cap1.release()
cv2.destroyAllWindows()