import cv2
import sys
import os
import time


cap = cv2.VideoCapture('v4l2src device=/dev/video0 ! video/x-raw, framerate=30/1, width=640, height=480 ! videoconvert ! appsink', cv2.CAP_GSTREAMER)
# cap.set(3, 1080)
# cap.set(4, 1920)

fc = 20.0
count = 0

codec = cv2.VideoWriter_fourcc(*"mp4v")
writing_video_dir="writing_video"
receive_video_dir="receive_video"

gst_out2 = "appsrc ! video/x-raw ! videoconvert ! x264enc tune=zerolatency bitrate=500 speed-preset=superfast ! rtph264pay config-interval=1 ! udpsink host=192.168.0.15 port=8041"


# 흑백은 마지막에 False로 컬러는 True
# writer1 = cv2.VideoWriter(gst_out,cv2.CAP_GSTREAMER,0,float(20),(640,480),True)
writer2 = cv2.VideoWriter(gst_out2,cv2.CAP_GSTREAMER,0,float(20),(640,480),True)

record_flag = False
init_flag = False
startTime=None
out = None
os.system(f"rm {writing_video_dir}/*")



while True:

    ret, frame = cap.read()
    cv2.imshow('test', frame)
    
    k = cv2.waitKey(1)
    if k == 27:
        break

    if not record_flag:
        record_flag=True
        startTime=time.time()
        tm=time.localtime(startTime)
        avi_name=f"{tm.tm_year}.{tm.tm_mon}.{tm.tm_mday}.{tm.tm_hour}:{tm.tm_min}:{tm.tm_sec}"
        # out = cv2.VideoWriter(f'{count}.avi', codec, fc, (int(cap.get(3)), int(cap.get(4))))
        out = cv2.VideoWriter(f'{writing_video_dir}/{avi_name}.mp4', codec, fc, (int(cap.get(3)), int(cap.get(4))))

    if startTime!=None and record_flag:

        if time.time()-startTime<5:
            out.write(frame)
        else:
            record_flag=False
            out.release()
            print("Saved")
            os.system(f"mv {writing_video_dir}/* {receive_video_dir}/")
    
    writer2.write(frame)
    
cap.release()
out.release()
cv2.destroyAllWindows()
os.system(f"rm {writing_video_dir}/*")
