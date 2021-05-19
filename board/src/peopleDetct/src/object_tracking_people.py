from tracking import Tracker, Trackable
import cv2
import numpy as np
import time

frame_size = 416
frame_count = 0
min_confidence = 0.5
font=cv2.FONT_HERSHEY_SIMPLEX

height = 0
width = 0
fpsFilt=0

trackers = []
trackables = {}

#file_name = './video/test3.mp4'
output_name = './output/output_test4.mp4'

# Load Yolo
net = cv2.dnn.readNet("./model/yolov4-tiny.weights", "./cfg/yolov4-tiny.cfg")
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
# initialize Tracker
tracker = Tracker()

# initialize the video writer
writer = None
writer_frame_count = 0
videonumber = 0

#gst_out2 = "appsrc ! video/x-raw ! videoconvert ! x264enc tune=zerolatency bitrate=100 speed-preset=superfast ! rtph264pay config-interval=1 ! udpsink host=192.168.0.46 port=10000 sync=false"

#writer2 =cv2.VideoWriter(gst_out2,cv2.CAP_GSTREAMER,0,float(12),(640,480),True)

def writeFrame(img):
    # use global variable, writer
    global writer
    global writer_frame_count
    global videonumber
    output_name = f"./output/outputvideo_{videonumber}.mp4"
    
    if writer_frame_count >= 120 or writer_frame_count <= 30:
        writer = None
        videonumber += 1
        write_frame_count = 0
        
    if writer is None and output_name is not None:
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        writer = cv2.VideoWriter(output_name, fourcc, 6, (img.shape[1], img.shape[0]),True)
        
    if writer is not None:
        writer.write(img)
        writer_frame_count += 1


vs = cv2.VideoCapture('v4l2src device=/dev/video0 ! video/x-raw, format=YUY2, framerate=30/1, width=640, height=480 ! videoconvert ! appsink', cv2.CAP_GSTREAMER)

#vs = cv2.VideoCapture(file_name)
# loop over the frames from the video stream
cp_frame = np.zeros((480,640,3), dtype=np.uint8)
fps_rate = vs.get(cv2.CAP_PROP_FPS)
#prev_time = 0
while True:
        ret, frame = vs.read()
        #cp_frame = frame.copy()

        #print(fps_rate)
        if frame is None:
            print('### No more frame ###')
            break
        # Start time capture
        frame_count += 1
        start_time = time.time()
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
                if class_id == 0 and confidence > min_confidence:

                    # Object detected
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    # Rectangle coordinates
                    x = int(center_x - w / 2) # 시작점의 x
                    y = int(center_y - h / 2) # 시작점의 y

                    boxes.append([x, y, w, h]) # 배열로 계속 넣어줌.

                    confidences.append(float(confidence))

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, min_confidence, 0.4) # 박스 중복을 줄여주는 거.
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                rects.append([x, y, x+w, y+h]) # 이 박스안에 중복된 내용이 있을수도 없을수도.
                label = '{:,.2%}'.format(confidences[i])
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1) # 박스처리해줌.
                cv2.putText(frame, label, (x + 5, y + 15), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 1)

        # use Tracker
        objects = tracker.update(rects)
        total = len(objects)
        # loop over the trackable objects
        # 아디하고 centroid 좌표가 온다.
        for (objectID, centroid) in objects.items():
                # check if a trackable object exists with the object ID
                # 트랙킹 되고 있는 알고리즘.
                trackable = trackables.get(objectID, None)

                # 아디 값 오면 trackable이라는 객체가 생성됨.
                if trackable is None:
                        trackable = Trackable(objectID, centroid)


                # store the trackable object in our dictionary
                trackables[objectID] = trackable
                text = "ID {}".format(objectID)
                cv2.putText(frame, text, (centroid[0] + 10, centroid[1] + 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                cv2.circle(frame, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)

        info = [
            ("total", total),
        ]

        # loop over the info tuples and draw them on our frame
        for (i, (k, v)) in enumerate(info):
            text = "{}: {}".format(k, v)
            cv2.putText(frame, text, (10, height - ((i * 20) + 20)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        if total >= 1:
            writeFrame(frame)

        # show the output frame
        dt=time.time()-start_time
        timeStamp=time.time()
        fps=1/dt
        fpsFilt=.9*fpsFilt + .1*fps
        #print(str(round(fps,1))+' fps')
        cv2.putText(frame,str(round(fpsFilt,1))+' fps',(0,30),font,1,(0,0,255),2)
        
        cv2.putText(frame, str(writer_frame_count) + ' frame', (10, height - ((i * 20) + 50)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
        cv2.imshow("Frame", frame)
        frame_time = time.time() - start_time
        print("Frame {} time {}".format(frame_count, frame_time))
        
        key = cv2.waitKey(1) & 0xFF

        #if total >=1:
            #writer2.write(cp_frame)
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
                break

vs.release()
writer.release()
cv2.destroyAllWindows()
