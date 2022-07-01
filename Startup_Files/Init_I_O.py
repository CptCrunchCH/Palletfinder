import RPi.GPIO as GPIO
import time

#Pin Definitions
Digital_Out_0 = 43 # Digital_Out_0
Digital_Out_1 = 44 # Digital_Out_1

GPIO.setmode(GPIO.BCM)  # BCM pin-numbering scheme from Raspberry Pi
GPIO.setup(Digital_Out_0, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Digital_Out_1, GPIO.OUT, initial=GPIO.LOW)