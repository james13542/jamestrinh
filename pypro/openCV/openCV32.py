import cv2
print(cv2.__version__)
import numpy as np
from adafruit_servokit import ServoKit
kit=ServoKit(channels=16)

pan=90
leftm = pan
rightm = pan
#tilt=90
kit.servo[0].angle=leftm
kit.servo[1].angle=rightm

def nothing(x):
    pass

cv2.namedWindow('Trackbars')
cv2.moveWindow('Trackbars',1320,0)

cv2.createTrackbar('hueLower', 'Trackbars',96,179,nothing)
cv2.createTrackbar('hueUpper', 'Trackbars',120,179,nothing)

cv2.createTrackbar('hue2Lower', 'Trackbars',50,179,nothing)
cv2.createTrackbar('hue2Upper', 'Trackbars',0,179,nothing)

cv2.createTrackbar('satLow', 'Trackbars',157,255,nothing)
cv2.createTrackbar('satHigh', 'Trackbars',255,255,nothing)
cv2.createTrackbar('valLow','Trackbars',100,255,nothing)
cv2.createTrackbar('valHigh','Trackbars',255,255,nothing)


dispW=640
dispH=480
flip=2
#Uncomment These next Two Line for Pi Camera
#camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
#cam= cv2.VideoCapture(camSet)

#Or, if you have a WEB cam, uncomment the next line
#(If it does not work, try setting to '1' instead of '0')
cam=cv2.VideoCapture(0)
width=cam.get(cv2.CAP_PROP_FRAME_WIDTH)
height=cam.get(cv2.CAP_PROP_FRAME_HEIGHT)
print('width:',width,'height:',height)
while True:   
    ret, frame = cam.read()
    #frame=cv2.imread('smarties.png')

    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    hueLow=cv2.getTrackbarPos('hueLower', 'Trackbars')
    hueUp=cv2.getTrackbarPos('hueUpper', 'Trackbars')

    hue2Low=cv2.getTrackbarPos('hue2Lower', 'Trackbars')
    hue2Up=cv2.getTrackbarPos('hue2Upper', 'Trackbars')

    Ls=cv2.getTrackbarPos('satLow', 'Trackbars')
    Us=cv2.getTrackbarPos('satHigh', 'Trackbars')

    Lv=cv2.getTrackbarPos('valLow', 'Trackbars')
    Uv=cv2.getTrackbarPos('valHigh', 'Trackbars')

    l_b=np.array([hueLow,Ls,Lv])
    u_b=np.array([hueUp,Us,Uv])

    l_b2=np.array([hue2Low,Ls,Lv])
    u_b2=np.array([hue2Up,Us,Uv])

    FGmask=cv2.inRange(hsv,l_b,u_b)
    FGmask2=cv2.inRange(hsv,l_b2,u_b2)
    FGmaskComp=cv2.add(FGmask,FGmask2)
    cv2.imshow('FGmaskComp',FGmaskComp)
    cv2.moveWindow('FGmaskComp',0,530)

    contours,_=cv2.findContours(FGmaskComp,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    contours=sorted(contours,key=lambda x:cv2.contourArea(x),reverse=True)
    for cnt in contours:
        area=cv2.contourArea(cnt)
        (x,y,w,h)=cv2.boundingRect(cnt)
        if area>=50:
            #cv2.drawContours(frame,[cnt],0,(255,0,0),3)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),3)
            objX=x+w/2
            objY=y+h/2
            errorPan=objX-width/2
            errorTilt=objY-height/2
            
            if errorPan>100:
                leftm=180
                rightm=90
            if  errorPan<-100:
                rightm=0
                leftm=90
            if 100>errorPan>-100:
                rightm=0
                leftm=180
            """
            if 180>errorPan>120:
                leftm=180
                rightm=90
            if  50>errorPan>0:
                rightm=0
                leftm=90
            if 120>errorPan>50:
                rightm=90
                leftm=90
            
            if errorPan>105:
                                                                 
            if errorPan<75:
                rightm=pan-errorPan/75
                leftm=0
            
            if abs(errorTilt)>15:
                tilt=tilt-errorTilt/75
            """

            if pan>180:
                leftm = 90
                rightm = 0
                print("Pan Out of  Range")   
            if pan<0:
                rightm = 90
                leftm = 0
                print("Pan Out of  Range") 
            """
            if tilt>180:
                tilt=90
                print("Tilt Out of  Range") 
            if tilt<0:
                tilt=0
                print("Tilt Out of  Range")                 
            """
            kit.servo[0].angle=leftm
            kit.servo[1].angle=rightm
            break        

    cv2.imshow('nanoCam',frame)
    cv2.moveWindow('nanoCam',0,0)
    

    if cv2.waitKey(1)==ord('q'):
        break
cam.release()
cv2.destroyAllWindows()