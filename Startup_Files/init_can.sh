#!/bin/bash
sudo modprobe can
sudo modprobe can-raw
sudo modprobe mttcan
sudo ip link set can0 up type can bitrate 250000
sudo ifconfig can0 txqueuelen 1000

