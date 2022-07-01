sudo docker kill $(docker ps -q)
sudo docker container rm Palletfinder

sudo docker run --runtime nvidia -itd --name=Palletfinder --volume ~/Palletfinder:/home/Palletfinder nvcr.io/nvidia/l4t-ml:r32.6.1-py3

sudo docker exec -it Palletfinder /bin/bash -c "chmod 777 /home/Palletfinder/01_Pytorch/Dataset/Dataset.py"

sudo docker exec -it Palletfinder /bin/bash -c "chmod +x /home/Palletfinder/01_Pytorch/Dataset/Dataset.py"

sudo docker exec -it Palletfinder /bin/bash -c "/usr/bin/python3.6 /home/Palletfinder/01_Pytorch/Dataset/Dataset.py"
