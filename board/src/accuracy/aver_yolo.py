import socket
import threading
import os
import buffer
import cv2
import numpy as np

frame_size = 416
frame_count = 0
min_confidence = 0.5

net = cv2.dnn.readNet("../PeopleDetect/model/yolov4-tiny.weights", "../PeopleDetect/cfg/yolov4-tiny.cfg")
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)



def isPeople(frame):
    (height, width) = frame.shape[:2]

    # draw a horizontal line in the center of the frame
    # construct a blob for YOLO model
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (frame_size, frame_size), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers) # object detection 나옴.
    rects = []

    confidences = []
    boxes = []

    # 사람일수도, 물체일수도.
    max_confidence = 0
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores) # 제일 높은 값을 찾음!!!
            confidence = scores[class_id] # 그 확률값이 얼마나.
            # Filter only 'person'
            #print("Confidence : " , confidence)
            
            if class_id == 0 and confidence > min_confidence:
                #print("Confidence : " , confidence)
                #print("***************DETECT*********************")
                max_confidence = max(max_confidence,confidence)
    
    return max_confidence
    
    #return 0

abnormal_path = './abnormal/'
normal_path = './normal/'
abnormal_filelist = os.listdir(abnormal_path)
normal_filelist =  os.listdir(normal_path)

aver_correct = []

for file_name in abnormal_filelist:
    #print(file_name)
    cap=cv2.VideoCapture(abnormal_path+file_name)
    ret,frame=cap.read()
    
    aver_correct.append(isPeople(frame))
    #print(isPeople(frame))

for file_name in normal_filelist:
    #print(file_name)
    cap=cv2.VideoCapture(normal_path+file_name)
    ret,frame=cap.read()
    
    aver_correct.append(isPeople(frame))
    #print(isPeople(frame))

print(aver_correct)
print(len(aver_correct))
res_sum = sum(float(sub) for sub in aver_correct)
print(res_sum / len(aver_correct))
        

