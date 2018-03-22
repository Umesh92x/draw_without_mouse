#Tracking red color of red led using image processing and performing drawing that erase automatically from another point after some time.
from collections import deque
import cv2
import urllib.request
import numpy as np
import sys
import pyautogui
import tkinter as tk
root = tk.Tk()
from pynput.mouse import Button,Controller
mouse=Controller()
sx = root.winfo_screenwidth()
sy = root.winfo_screenheight()
(camx,camy)=(420,233)
SCREEN_X, SCREEN_Y = pyautogui.size()

pts = deque(maxlen=64)

hoststr = "http://192.168.1.2:4747/mjpegfeed?640x480"

pyautogui.moveTo(900,800)
#hoststr = 'http://' + host
print ('Streaming ' + hoststr)
img = np.zeros((512,512,3), np.uint8)
#TOdo lower_blue = np.array([160,50,50],dtype=np.uint8)
# Todo uper_blue= np.array([179,255,255],dtype=np.uint8)

stream=urllib.request.urlopen(hoststr)
bytes=b''

#lower_blue=np.array([173,60,60],dtype='uint8')
#upper_blue=np.array([179,255,255],dtype='uint8')
ix=-1
iy=-1
lower_blue=np.array([136,87,111],dtype='uint8')
upper_blue=np.array([180,255,245],dtype='uint8')
while True:

    bytes+=stream.read(1024)
    #print(bytes)
    a = bytes.find(b'\xff\xd8')
    b = bytes.find(b'\xff\xd9')
    #print(a,b)

    if a!=-1 and b!=-1:
        #print(("hvghvbn"))
        jpg = bytes[a:b+2]
        bytes= bytes[b+2:]

        frame= cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.CV_32F)
        frame = cv2.resize(frame, (1000,800))
        frame=cv2.flip(frame,1)
        #cv2.imshow('hoststr', frame)
        #TODO

        #ret, frame = i.read()
        HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(HSV, lower_blue,upper_blue)
        HSV_red = cv2.bitwise_and(frame, frame, mask=mask)

        kernelOpen = np.ones((2, 2))
        kernelClose = np.ones((10, 10))
        opening = cv2.morphologyEx(HSV_red, cv2.MORPH_OPEN, kernelOpen)
        closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernelClose)


        maskE = cv2.erode(mask, None, iterations=0)
        maskD=cv2.dilate(maskE,None,iterations=0)


        _, cnts, h = cv2.findContours(maskD.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for i in range(len(cnts)):
            c = max(cnts, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(c)
            ((x1, y1), radius) = cv2.minEnclosingCircle(c)
            x1 = int(x + w / 2)
            y1 = int(y + h / 2)
            center=(x1,y1)

            pts.appendleft(center)

            #if radius > 0:
            # cv2.circle(frame,(int(x1),int(y1)),int(radius),(0,0,255),2)
            cv2.circle(frame, (x, y), 5, (255, 0, 0), -1)
            #mouseLoc1,mouseLoc2 = ((cx * sx / camx), (cmouy * sy / camy))
            #print(mouseLoc1,'and',mouseLoc2)
            mouse.position =(int(x1),int(y1))
            #cv2.moveWindow('frame', int(2*cx),int(2*cy))
            #pyautogui.moveTo(mouseLoc)
            #cv2.moveWindow('frame',200,200)
            for i in range(1, len(pts)):
                # if either of the tracked points are None, ignore
                # them
                if pts[i - 1] is None or pts[i] is None:
                    continue

                # otherwise, compute the thickness of the line and
                # draw the connecting lines
                #thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
                cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), 5)
#Todo (led not detected ,
                # show the frame to our screen

        if cnts==0 or cnts==None:
            for i in range(1, len(pts)):
                # if either of the tracked points are None, ignore
                # them
                if pts[i - 1] is None or pts[i] is None:
                    continue

                # otherwise, compute the thickness of the line and
                # draw the connecting lines
                #thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
                cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), 5)
                cv2.imshow("Frame", frame)

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(10) & 0xFF

            # if the 'q' key is pressed, stop the loop
        if key == ord("q"):
            break
        # cleanup the camera and close any open windows
            camera.release()
            cv2.destroyAllWindows()
            
if __name__=='__main__':
    print('Executed')
  
