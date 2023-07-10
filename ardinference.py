import cv2
import serial
import jetson.inference
import jetson.utils
import time
print(cv2.__version__)
import numpy as np

pan=90
leftm = pan
rightm = pan


def nothing(x):
    pass

"""
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
"""

timeStamp=time.time()
fpsFilt=0
net=jetson.inference.detectNet('ssd-mobilenet-v2',threshold=.5)
dispW=1280
dispH=720
sstring= 'S\n'
sstringold= 'S\n'
flip=2
count = 0
seekitem = 'cell phone'
font=cv2.FONT_HERSHEY_SIMPLEX
#Uncomment These next Two Line for Pi Camera
#camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
#cam= cv2.VideoCapture(camSet)

#Or, if you have a WEB cam, uncomment the next line
#(If it does not work, try setting to '1' instead of '0')
cam=cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, dispW)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, dispH)
width=cam.get(cv2.CAP_PROP_FRAME_WIDTH)
height=cam.get(cv2.CAP_PROP_FRAME_HEIGHT)
print('width:',width,'height:',height)
with serial.Serial('/dev/ttyACM0', 115200, write_timeout = .1) as ser:
    time.sleep(1)
    while True:   
        #img, width, height= cam.CaptureRGBA()
        _,img = cam.read()
        height=img.shape[0]
        width=img.shape[1]
        ser.flush()
        count += 1
        frame=cv2.cvtColor(img,cv2.COLOR_BGR2RGBA).astype(np.float32)
        frame=jetson.utils.cudaFromNumpy(frame)
        detections=net.Detect(frame, width, height)
        for detect in detections:
            #print(detect)
            ID=detect.ClassID
            top=detect.Top
            left=detect.Left
            bottom=detect.Bottom
            right=detect.Right
            item=net.GetClassDesc(ID)
            print(item,top,left,bottom,right)
            x = top
            y = left
            w = right - left
            h = bottom - top
            area = (right - left) * (bottom - top)
            if area>=50 and item == seekitem:
                #cv2.drawContours(frame,detect,0,(255,0,0),3)
                cv2.rectangle(img,(int(y),int(x)),(int(y+w),int(x+h)),(255,0,0),3)
                
                objX=y+w/2
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
                break

            elif (area >= 300) and item == seekitem: 
                sstring = 'C\n'
                seekitem = 'mouse'   
            else :
                sstring = 'S\n'
                #ser.write(bytes('S\n','utf-8'))
        if (not detections):
            sstring = 'S\n'
        if (sstring != sstringold):
            ser.flush()
            print("Sending" + sstring)
            try: 
                ser.write(sstring.encode())
                #time.sleep(.1)
            except: 
                print('help')
                ser = serial.Serial('/dev/ttyACM0', 115200, write_timeout = .1)
            sstringold = sstring
        #display.RenderOnce(img,width,height)
        
        dt=time.time()-timeStamp
        timeStamp=time.time()
        fps=1/dt
        fpsFilt=.9*fpsFilt + .1*fps
        #print(str(round(fps,1))+' fps')
        cv2.putText(img,str(round(fpsFilt,1))+' fps',(0,30),font,1,(0,0,255),2)
        
        cv2.imshow('detCam',img)
        cv2.moveWindow('detCam',0,0)
        if cv2.waitKey(1)==ord('q'):
            break
ser.close()
cam.release()
cv2.destroyAllWindows()