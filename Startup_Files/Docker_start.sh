# Use docker to read model to make Prediction
#   First end all running docker container named Palltfinder
#   sudo docker kill $(docker ps -q)
#   sudo docker container rm Palletfinder
#   Run nvidia docker
sudo docker run --restart=always --runtime nvidia -itd --name=Palletfinder --volume ~/Palletfinder:/home/Palletfinder nvcr.io/nvidia/l4t-ml:r32.6.1-py3

# Start Python file

sudo docker exec -it Palletfinder /bin/bash -c "chmod 777 /home/Palletfinder/03_Make_Prediction/Makeprediction.py"
sudo docker exec -it Palletfinder /bin/bash -c "chmod +x /home/Palletfinder/03_Make_Prediction/Makeprediction.py"
sudo docker exec -it Palletfinder /bin/bash -c "/usr/bin/python3.6 /home/Palletfinder/03_Make_Prediction/Makeprediction.py"