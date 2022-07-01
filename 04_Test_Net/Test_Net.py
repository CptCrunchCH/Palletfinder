import joblib
import torch
import argparse
import torch.nn as nn
import torch.nn.functional as F
from PIL import Image
from torchvision import transforms

class model(nn.Module):
    def __init__(self):
        super(model,self).__init__()
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=2, kernel_size= 2)     # three channels in  6 channels out 
        self.pool = nn.MaxPool2d(4,4)
        self.conv2 = nn.Conv2d(in_channels=2, out_channels=4, kernel_size= 10)  
        self.fc1 = nn.Linear(1352,1000)
        self.fc2 = nn.Linear(1000,500)
        self.fc3 = nn.Linear(500,5)
                
    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = torch.flatten(x,1)                  # flatten all dimensions except for batch
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

if __name__ == '__main__':

    # construct the argument parser and parse the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--img', default='1.jpg', type=str,
        help='path for the image to test on')
    args = vars(parser.parse_args())

    lb = joblib.load('home/Palletfinder/04_Test_Net/output/lb.pkl')

    model = model()
    model.load_state_dict(torch.load('home/Palletfinder/04_Test_Net/output/model.pth'))

    path = 'home/Palletfinder/04_Test_Net/inputs/2_Palette_55.jpg'
    aug = transforms.Compose([
                transforms.Resize(256),
                transforms.ToTensor(),

            ])
    image = Image.open(path)
    image_copy = image.copy()
    image = aug(img=image)
    image = torch.tensor(image, dtype=torch.float)
    image = image[None,:,:,:]

    outputs = model(image)
    _, preds = torch.max(outputs.data, 1)
    print(f"Predicted output: {lb.classes_[preds]}")