import cv2
import serial
import time
print(cv2.__version__)
import numpy as np

pan=90
leftm = pan
rightm = pan


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
sstring= 'S\n'
sstringold= 'S\n'
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
with serial.Serial('/dev/ttyACM0', 115200 , timeout=1) as ser:

    while True:   
        ret, frame = cam.read()
        #frame=cv2.imread('smarties.png')

        hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        #blue is 96 to 120 orange is 16 to 30
        
        hueLow=96
        hueUp=120

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
                cv2.rectangle(frame,x,y,x+w,y+h,(255,0,0),3)
                objX=x+w/2
                errorPan=objX-width/2
                
                if errorPan>100:
                    leftm=180
                    rightm=90
                    sstring = 'R\n'
                    #ser.write(bytes('R\n','utf-8'))
                elif errorPan<-100:
                    rightm=0
                    leftm=90
                    sstring = 'L\n'
                    #ser.write(bytes('L\n','utf-8'))
                elif 100>errorPan>-100:
                    rightm=90
                    leftm=90
                    sstring = 'G\n'
                    #ser.write(bytes('G\n','utf-8'))

                elif pan>180:
                    leftm = 90
                    rightm = 0
                    print("Pan Out of  Range")  
                    sstring = 'R\n'
                    #ser.write(bytes('R\n','utf-8'))

                elif pan<0:
                    rightm = 90
                    leftm = 180
                    print("Pan Out of  Range") 
                    sstring = 'L\n'
                    #ser.write(bytes('L\n','utf-8'))
                break  
            elif (area >= 200): 
                sstring = 'C\n'
                hueLow=16
                hueUp=30
            else :
                sstring = 'S\n'
                #ser.write(bytes('S\n','utf-8'))
        if (not contours):
            sstring = 'S\n'
        if (sstring != sstringold):
            ser.write(bytes(sstring,'utf-8'))
            sstringold = sstring
        cv2.imshow('nanoCam',frame)
        cv2.moveWindow('nanoCam',0,0)
        
        if cv2.waitKey(1)==ord('q'):
            break
cam.release()
cv2.destroyAllWindows()


