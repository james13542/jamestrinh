import cv2
print(cv2.__version__)
dispW=320
dispH=240
flip=2
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cam=cv2.VideoCapture(0)
i = 0
j=0
negi =1
negj = 1
while True:
    ret, frame=cam.read()
    frame=cv2.rectangle(frame,(140,100),(180,140),(255,0,0),4)
    frame=cv2.circle(frame,(320,240),50,(0,0,255),-1)
    fnt=cv2.FONT_HERSHEY_DUPLEX
    frame=cv2.putText(frame, 'My First Test', (300,300),fnt, 1, (255,0,150),2)
    
    if (i == dispH) :
        negi = -1
    
    if (i == 0) :
        negi = 1
    
    if (j == dispW) :
        negj = -1
    
    if (j == 0) :
        negj = 1
    

    if (negi == 1) :
        i += 5
    else :
        i -=5
    
    if (negj == 1) :
        j += 5
    else :
        j -=5
    
    frame=cv2.circle(frame,(i, j),50,(0,0,255),-1)
    
    cv2.imshow('piCam',frame)
    if cv2.waitKey(1)==ord('q'):
        break
cam.release()
cv2.destroyAllWindows()
