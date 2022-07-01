# Use docker to read model to make Prediction
#   First end all running docker container named Palltfinder
#   sudo docker kill $(docker ps -q)
#   sudo docker container rm Palletfinder
#   Run nvidia docker
sudo docker run --restart=always --runtime nvidia -itd --name=Palletfinder --volume ~/Palletfinder:/home/Palletfinder nvcr.io/nvidia/l4t-ml:r32.6.1-py3