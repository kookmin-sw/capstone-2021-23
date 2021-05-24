import jetson.inference
import jetson.utils
import time
import cv2
import numpy as np 
import os
 
timeStamp=time.time()
fpsFilt=0
net=jetson.inference.detectNet('ssd-mobilenet-v2',threshold=0.5)
dispW=640
dispH=480
flip=2
font=cv2.FONT_HERSHEY_SIMPLEX
 
# Gstreamer code for improvded Raspberry Pi Camera Quality
#camSet='nvarguscamerasrc wbmode=3 tnr-mode=2 tnr-strength=1 ee-mode=2 ee-strength=1 ! video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! videobalance contrast=1.5 brightness=-.2 saturation=1.2 ! appsink'
#cam=cv2.VideoCapture(camSet)
#cam=jetson.utils.gstCamera(dispW,dispH,'0')
#cam = cv2.VideoCapture('v4l2src device=/dev/video0 ! video/x-raw, format=YUY2, framerate=30/1, width=640, height=480 ! videoconvert ! appsink', cv2.CAP_GSTREAMER)
#cam=cv2.VideoCapture('/dev/video0')

#cam = cv2.VideoCapture('./test4.mp4')
#cam.set(cv2.CAP_PROP_FRAME_WIDTH, dispW)
#cam.set(cv2.CAP_PROP_FRAME_HEIGHT, dispH)



#camSet='v4l2src device="/dev/video0" ! video/x-raw, width=640, height=480 ! nvvidconv ! "video/x-raw(memory:NVMM)" ! nvvidconv ! nvstabilize crop-margin=0.1 queue-size=5 ! nvvidconv ! "video/x-raw(memory:NVMM)" ! nvvidconv ! appsink'
#cam=cv2.VideoCapture(camSet) 
#cam=jetson.utils.gstCamera(640,480,'0')
#cam=jetson.utils.gstCamera(dispW,dispH,'/dev/video0')
#display=jetson.utils.glDisplay()
#while display.IsOpen():
abnormal_path = './abnormal/'
normal_path = './normal/'
abnormal_filelist = os.listdir(abnormal_path)
normal_filelist =  os.listdir(normal_path)

aver_correct = []

for file_name in abnormal_filelist:
    #print(file_name)
    cap=cv2.VideoCapture(abnormal_path+file_name)

    _,img = cap.read()
    height=img.shape[0]
    width=img.shape[1]
 
    frame=cv2.cvtColor(img,cv2.COLOR_BGR2RGBA).astype(np.float32)
    frame=jetson.utils.cudaFromNumpy(frame)
 
    detections=net.Detect(frame, width, height)
    max_confidence = 0
    for detect in detections:
        #print(detect)
        aver_tmp = []
        ID=detect.ClassID
        #print(file_name, ID)
        
        if ID == 1:
            top=int(detect.Top)
            left=int(detect.Left)
            bottom=int(detect.Bottom)
            right=int(detect.Right)
            item=net.GetClassDesc(ID)
            confidence=detect.Confidence
            instance = detect.Instance
            #aver_tmp.append(confidence)
            
            print(file_name,confidence, instance)
            max_confidence = max(max_confidence, confidence)
            #print(item,top,left,bottom,right)
    print(max_confidence)
    aver_correct.append(max_confidence)

for file_name in normal_filelist:
    #print(file_name)
    cap=cv2.VideoCapture(normal_path+file_name)

    _,img = cap.read()
    height=img.shape[0]
    width=img.shape[1]
 
    frame=cv2.cvtColor(img,cv2.COLOR_BGR2RGBA).astype(np.float32)
    frame=jetson.utils.cudaFromNumpy(frame)
 
    detections=net.Detect(frame, width, height)
    max_confidence2 = 0
    for detect in detections:
        #print(detect)
        aver_tmp = []
        ID=detect.ClassID
        #print(file_name, ID)
        
        if ID == 1:
            top=int(detect.Top)
            left=int(detect.Left)
            bottom=int(detect.Bottom)
            right=int(detect.Right)
            item=net.GetClassDesc(ID)
            confidence=detect.Confidence
            instance = detect.Instance
            #aver_tmp.append(confidence)
            
            print(file_name,confidence, instance)
            max_confidence2 = max(max_confidence2, confidence)
            #print(item,top,left,bottom,right)
    print(max_confidence2)
    aver_correct.append(max_confidence2)
        

#print(aver_correct)
res_sum = sum(float(sub) for sub in aver_correct)
print(len(aver_correct))
print(res_sum / len(aver_correct))
