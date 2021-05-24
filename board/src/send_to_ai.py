import socket
import threading
import os
import buffer
import cv2
import numpy as np

#HOST = '192.168.0.18'
#HOST = '127.0.0.1'
HOST = '58.142.223.232'
PORT = 2345

frame_size = 416
frame_count = 0
min_confidence = 0.25

net = cv2.dnn.readNet("./peopleDetect/model/yolov4-tiny.weights", "./peopleDetect/cfg/yolov4-tiny.cfg")
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
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores) # 제일 높은 값을 찾음!!!
            confidence = scores[class_id] # 그 확률값이 얼마나.
            # Filter only 'person'
            #print("Confidence : " , confidence)
            if class_id == 0 and confidence > min_confidence:
                print("Confidence : " , confidence)
                print("***************DETECT*********************")
                return True
    
    return False

path = './peopleDetect/receive_video/'
os.system(f"rm ./peopleDetect/receive_video/*.mp4")
while True:
    #os.system(f"rm ./receive_video/*.mp4")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    
    with s:
        while True:
            files_to_send = os.listdir(path)

            if len(files_to_send) >= 1:
                break
            else:
                continue


        sbuf = buffer.Buffer(s)

        hash_type = 'a'

        #files = os.listdir(path)

        for file_name in files_to_send:
            print(file_name)
            cap=cv2.VideoCapture(path+file_name)
            ret,frame=cap.read()
            
            if isPeople(frame):
                sbuf.put_utf8(hash_type)
                sbuf.put_utf8(file_name)

                file_size = os.path.getsize(path + file_name)
                sbuf.put_utf8(str(file_size))
                
                with open(path + file_name, 'rb') as f:
                    sbuf.put_bytes(f.read())
                print('File Sent')
            
            else:
                continue

        os.system(f"rm ./peopleDetect/receive_video/*.mp4")
