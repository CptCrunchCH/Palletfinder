#!/bin/bash

# Snap Image:
#   Make an Executable Python File:
chmod 777 /home/nvidia/Palletfinder/05_Make_Prediction/Snap_Images.py
chmod +x /home/nvidia/Palletfinder/05_Make_Prediction/Snap_Images.py
#   Snap image and save in /05_Make_Prediction/Images
python3 /home/nvidia/Palletfinder/05_Make_Prediction/Snap_Images.py


# Use docker to read model to make Prediction
#   First end all running docker container named Palltfinder
sudo docker kill $(docker ps -q)
sudo docker container rm Palletfinder
#   Run nvidia docker
sudo docker run --runtime nvidia -itd --name=Palletfinder --volume ~/Palletfinder:/home/Palletfinder nvcr.io/nvidia/l4t-ml:r32.6.1-py3
#   Execute Prediction python file in docker
sudo docker exec -it Palletfinder /bin/bash -c "chmod 777 /home/Palletfinder/05_Make_Prediction/Makeprediction.py"
sudo docker exec -it Palletfinder /bin/bash -c "chmod +x /home/Palletfinder/05_Make_Prediction/Makeprediction.py"
sudo docker exec -it Palletfinder /bin/bash -c "/usr/bin/python3.6 /home/Palletfinder/05_Make_Prediction/Makeprediction.py"
