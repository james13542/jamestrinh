import cv2
print(cv2.__version__)
evt=-1
coord=[]
def click(event,x,y,flags,params):
    global pnt
    global evt
    if event==cv2.EVENT_LBUTTONDOWN:
        print('Mouse Event Was:  ', event)
        print(x, ',', y)
        pnt=(x,y)
        coord.append(pnt)
        print(coord)
        evt=event
    if event==cv2.EVENT_RBUTTONDOWN:
        print('Mouse Event Was:  ', event)
        print(x, ',', y)
        blue =frame[y,x,0]
        green =frame[y,x,1]
        red =frame[y,x,2]
        print(blue,green,red)
        evt=event
dispW=320
dispH=240
flip=2

cv2.namedWindow('nanoCam')
cv2.setMouseCallback('nanoCam',click)


camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cam=cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, dispW)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, dispH)

while True:
    ret, frame=cam.read()
    for pnts in coord:
        cv2.circle(frame,pnts,5,(0,50,200),-1)
        font=cv2.FONT_HERSHEY_PLAIN
        myStr=str(pnts)
        cv2.putText(frame,myStr,pnts,font,1,(255,0,0),2)
    """
    if evt==1:
        cv2.circle(frame,pnt,5,(0,100,0),-1)
        font=cv2.FONT_HERSHEY_PLAIN
        myStr=str(pnt)
        cv2.putText(frame,myStr,pnt,font,1,(255,0,0),2)
    """
    cv2.imshow('nanoCam',frame)
    cv2.moveWindow('nanoCam',0,0)
    keyEvent = cv2.waitKey(1)
    if keyEvent==ord('q'):
        break
    if keyEvent==ord('c'):
        coord=[]
cam.release()
cv2.destroyAllWindows()
