01_Kamaera:
    - Includes all images, which were used for the Training as for the Test and Validation
    - As well as a python script, which can be used to snap pictures with the Palletfinder system (Bilder_aufnehmen_speichern.py)
    - Includes all Functions to read the camera (V4l2_Functions.py)
    - And a Testfile to snap images or show live camera (Import_Camera.py)

02_IO: 
    - Includes a simple python File, which toggles the LED connected on the outputs 43 & 44

03_Make_Prediction:
    - Images:
        - Includes the recently snaped images
    - output:
        - Includes Label Names
        - And Trained Model
    - Makeprediction.py: Loads Model and drives the snapped image through it and predicts the number of pallets
    - Snap_Images.py: Snaps two images and saves them to /Images
    - V4l2_Functoins.py: Used functions in Snap_Images.py

