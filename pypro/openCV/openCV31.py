import cv2
import time
print(cv2.__version__)
import numpy as np
from adafruit_servokit import ServoKit
myKit=ServoKit(channels=16)

myKit.servo[0].angle = 90
myKit.servo[1].angle = 90
cam=cv2.VideoCapture(0)
width=cam.get(cv2.CAP_PROP_FRAME_WIDTH)
height=cam.get(cv2.CAP_PROP_FRAME_HEIGHT)
while (True):
    et, frame=cam.read()
    cv2.imshow('nanoCam',frame)
    myKit.servo[0].angle = 0
    myKit.servo[1].angle = 0
    time.sleep(.1)
    myKit.servo[0].angle = 90
    myKit.servo[1].angle = 90
    time.sleep(.1)
    #myKit.servo[0].angle = 0
    #myKit.servo[1].angle = 0
    if cv2.waitKey(1)==ord('q'):
        myKit.servo[0].angle = 90
        myKit.servo[1].angle = 90
        break
cam.release()
cv2.destroyAllWindows()