#!/bin/bash
whoami
sudo docker stop Palletfinder
sudo docker rm Palletfinder
sudo docker run --restart=always --runtime nvidia -itd --name=Palletfinder --volume ~/Palletfinder:/home/Palletfinder nvcr.io/nvidia/l4t-ml:r32.6.1-py3
sudo docker exec Palletfinder /bin/bash -c "pip3 install imutils"
sudo docker exec Palletfinder /bin/bash -c "chmod 777 /home/Palletfinder/03_Make_Prediction/Makeprediction.py"
sudo docker exec Palletfinder /bin/bash -c "chmod +x /home/Palletfinder/03_Make_Prediction/Makeprediction.py"
sudo docker exec Palletfinder /bin/bash -c "/usr/bin/python3.6 /home/Palletfinder/03_Make_Prediction/Prediction_V2.py"