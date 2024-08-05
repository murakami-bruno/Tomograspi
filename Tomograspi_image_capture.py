#Imports
from time import sleep
import RPi.GPIO as GPIO
from picamera2 import Picamera2
import numpy as np
from datetime import datetime
import os

#Functions

def Rotates_CW_Step_Motor(segm_steps, count = False):
    
    GPIO.output(DIR, CW)
    for i in range(segm_steps):
        GPIO.output(STEP, GPIO.HIGH)
        sleep(step_delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(step_delay)
        if count == True:
            print(i)

def capture_jpg(n_for_sinogram):

    now = datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(folder_name, f"image_{timestamp}.jpg")
    camera.capture_file(filename)    
    print("Photo {0} Taken: Image_{1}".format(n_for_sinogram+1,filename))


def Rotates_CCW_Step_Motor(step_count, count = False):
    
    GPIO.output(DIR, CCW)
    for i in range(step_count):
        GPIO.output(STEP, GPIO.HIGH)
        sleep(step_delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(step_delay)
        if count == True:
            print(i)

#GPIO BCM OUTPUT
DIR = 12
STEP = 19

#Stepper Motor Parameters
SPR = 200 #Steps per Rotation
n_for_sinogram = 25  #number of angles of rotation
step_delay = 0.01 #0.02~0.0003 - Delay between steps
step_counting = False #enable if you want to display the steps counting

#picamera2 Parameters
os.environ['LIBCAMERA_LOG_LEVELS'] = '4' #set warnings off
camera = Picamera2()
camera.configure(camera.create_still_configuration())

#Others Variables
step_count = SPR/2 # it's divided by 2 to make half of a revolution
CW = 1
CCW = 0
segm_steps = int(np.ceil(step_count/n_for_sinogram)) # the number of steps for each segment

#Create folder 
now = datetime.now()
timestamp = now.strftime("%Y%m%d_%H%M%S")
folder_name = f"folder_{n_for_sinogram}ang_{timestamp}"
os.makedirs(folder_name)
print("Folder created: {0}".format(folder_name))

#GPIO SETUP
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)

#Stepper motor info
print("Start")
sleep(0.5)
print("The motor will rotate {0} º/segment or {1} steps/segment.".format(1.8*segm_steps,segm_steps))
sleep(0.5)


#Start Camera
camera.start()

#Loop
for x in range(n_for_sinogram): # makes "n_for_sinogram" segmentations from "step_counting" steps  

    Rotates_CW_Step_Motor(segm_steps,step_counting)
    sleep(1)
    capture_jpg(x)
    sleep(2)

#End Camera
camera.stop()

#Stepperb motor info
sleep(0.5)
print("The motor rotated {0} º or {1} steps.".format(1.8*segm_steps*n_for_sinogram,segm_steps*n_for_sinogram))
sleep(2)
print("Starting Counterclockwise Rotation" )
sleep(0.5)

#Counterclockwise Rotation
Rotates_CCW_Step_Motor(n_for_sinogram*segm_steps,step_counting)

#End
print("End")
GPIO.cleanup()
