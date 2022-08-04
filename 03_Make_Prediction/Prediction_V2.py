import joblib
import torch
import argparse
import torch.nn as nn
import torch.nn.functional as F
from PIL import Image
from torchvision import transforms
import time
from os.path import exists
import os
from torch.nn import Dropout
from torch.nn import Linear
from torch.nn import ReLU
from torch.nn import Sequential
from torch.nn import Sigmoid
from torch.nn import Module
import torch.nn as nn
import torch.nn.functional as F
import cv2
import imutils
import pickle
import numpy as np

class ObjectDetector(Module):
    def __init__(self,baseModel,numClasses):
        super(ObjectDetector, self).__init__()
        self.baseModel = baseModel
        self.numClasses = numClasses
        self.regressor = Sequential(
            Linear(baseModel.fc.in_features, 128),
            ReLU(),
            Linear(128,64),
            ReLU(),
            Linear(64,32),
            ReLU(),
            Linear(32,4),
            Sigmoid()
        )
        self.classifier = Sequential(
            Linear(baseModel.fc.in_features, 512),
            ReLU(),
            Dropout(),
            Linear(512,512),
            ReLU(),
            Dropout(),
            Linear(512, self.numClasses),
        )
        self.baseModel.fc = Identity()
    def forward(self,x):
        features = self.baseModel(x)
        bboxes = self.regressor(features)
        classLoggits = self.classifier(features)
        return bboxes,classLoggits


model_path = '/home/Palletfinder/03_Make_Prediction/output/model_BB.pth'
pickle_path = '/home/Palletfinder/03_Make_Prediction/output/le.pickle'
path_frame_left = '/home/Palletfinder/03_Make_Prediction/Images/frame_left.png'
path_frame_right = '/home/Palletfinder/03_Make_Prediction/Images/frame_right.png'

if __name__ == '__main__':
    device = ('cuda:0' if torch.cuda.is_available() else 'cpu')
    print(f"Computation device: {device}")
    model = torch.load(model_path).to(device)
    model.eval()
    le = pickle.loads(open(pickle_path, "rb").read())

    transforms = transforms.Compose([
        transforms.ToPILImage(),
        transforms.ToTensor(),
        transforms.Grayscale(),
    ])
    print("Model loaded")
    while (1):
        while not(exists("/home/Palletfinder/03_Make_Prediction/output/Start_Prediction.txt")):
            time.sleep(0.1)          
            # if exists("test.txt"):
        os.remove("/home/Palletfinder/03_Make_Prediction/output/Start_Prediction.txt")
        print("[Info] Starting")
        start_time = time.time()
        print("[Info]Loading Pickle")

        # load the image, copy it, resize it, and
        # bring its channel dimension forward
        print("[Info] Reading Images")
        image_left = cv2.imread(path_frame_left)
        image_right = cv2.imread(path_frame_right)

        orig_left = image_left.copy()
        orig_right = image_right.copy()

        image_left = cv2.resize(image_left, (254, 254))
        image_right = cv2.resize(image_right, (254, 254))

        image_left = image_left.transpose((2, 0, 1))
        image_right = image_right.transpose((2, 0, 1))

        # convert image to PyTorch tensor, flash it to the
        # current device, and add a batch dimension
        image_left = torch.from_numpy(image_left)
        image_right = torch.from_numpy(image_right)

        image_left = transforms(image_left).to(device)
        image_right = transforms(image_right).to(device)

        image_left = image_left.unsqueeze(0)
        image_right = image_right.unsqueeze(0)

        image_left = image_left.expand(-1,3,-1,-1)
        image_right = image_right.expand(-1,3,-1,-1)
        print("[Info] Images Transformed")
        # predict the bounding box of the object along with the class
        # label
        (boxPreds_left, labelPreds_left) = model(image_left)
        (boxPreds_right, labelPreds_right) = model(image_right)
        
        (startX_left, startY_left, endX_left, endY_left) = boxPreds_left[0]
        (startX_right, startY_right, endX_right, endY_right) = boxPreds_right[0]

        # determine the class label with the largest predicted
        # probability
        labelPreds_left = torch.nn.Softmax(dim=-1)(labelPreds_left)
        labelPreds_right = torch.nn.Softmax(dim=-1)(labelPreds_right)
        i_left = labelPreds_left.argmax(dim=-1).cpu()
        i_right = labelPreds_right.argmax(dim=-1).cpu()
        
        label_left = le.inverse_transform(i_left)[0]
        label_right = le.inverse_transform(i_right)[0]
        print("[Info] Predictions Made")
            # resize the original image such that it fits on our screen, and
        # grab its dimensions
        orig_left = imutils.resize(orig_left, width=600)
        orig_right = imutils.resize(orig_right, width=600)
        (h_left, w_left) = orig_left.shape[:2]
        (h_right, w_right) = orig_right.shape[:2]
        # scale the predicted bounding box coordinates based on the image
        # dimensions
        startX_left = int(startX_left * w_left)
        startX_right = int(startX_right * w_right)
        startY_left = int(startY_left * h_left)
        startY_right = int(startY_right * h_right)
        endX_left = int(endX_left * w_left)
        endX_right = int(endX_right * w_right)
        endY_left = int(endY_left * h_left)
        endY_right = int(endY_right * h_right)
        print("[Info] Rectangle Createt")
        # draw the predicted bounding box and class label on the image
        y_left = startY_left - 10 if startY_left - 10 > 10 else startY_left + 10
        y_right = startY_right - 10 if startY_right - 10 > 10 else startY_right + 10

        cv2.putText(orig_left, label_left, (startX_left, y_left), cv2.FONT_HERSHEY_SIMPLEX,
            0.65, (0, 255, 0), 2)
        cv2.putText(orig_right, label_right, (startX_right, y_right), cv2.FONT_HERSHEY_SIMPLEX,
            0.65, (0, 255, 0), 2)

        cv2.rectangle(orig_left, (startX_left, startY_left), (endX_left, endY_left),
            (0, 255, 0), 2)
        cv2.rectangle(orig_right, (startX_right, startY_right), (endX_right, endY_right),
            (0, 255, 0), 2)
        print("[Info] Recrtangle Drawn")
        # show the output image 
        print(label_left)
        print(label_right)
        print(startX_left,startY_left,endX_left,endY_left)
        print(startX_right,startY_right,endX_right,endY_right)
        cv2.imwrite("/home/Palletfinder/03_Make_Prediction/output/Predictions/left_prediction.png", orig_left)
        cv2.imwrite("/home/Palletfinder/03_Make_Prediction/output/Predictions/right_prediction.png", orig_right)

        #Write Predictions to File
        File = open("/home/Palletfinder/03_Make_Prediction/output/Predictions/Label_left.txt","w")
        File.write(label_left)
        File.close()
        File = open("/home/Palletfinder/03_Make_Prediction/output/Predictions/Label_right.txt","w")
        File.write(label_right)
        File.close()
        
        
        File = open("/home/Palletfinder/03_Make_Prediction/output/Predictions/startX_left.txt","w")
        File.write(str(startX_left))
        File.close()
        File = open("/home/Palletfinder/03_Make_Prediction/output/Predictions/startX_right.txt","w")
        File.write(str(startX_right))
        File.close()

        File = open("/home/Palletfinder/03_Make_Prediction/output/Predictions/startY_left.txt","w")
        File.write(str(startY_left))
        File.close()
        File = open("/home/Palletfinder/03_Make_Prediction/output/Predictions/startY_right.txt","w")
        File.write(str(startY_right))
        File.close()
        
        File = open("/home/Palletfinder/03_Make_Prediction/output/Predictions/endX_left.txt","w")
        File.write(str(endX_left))
        File.close()
        File = open("/home/Palletfinder/03_Make_Prediction/output/Predictions/endX_right.txt","w")
        File.write(str(endX_right))
        File.close()
        
        File = open("/home/Palletfinder/03_Make_Prediction/output/Predictions/endY_left.txt","w")
        File.write(str(endY_left))
        File.close()
        File = open("/home/Palletfinder/03_Make_Prediction/output/Predictions/endY_right.txt","w")
        File.write(str(endY_right))
        File.close()
        time.sleep(0.01)
        print("[Info] Files Saved")