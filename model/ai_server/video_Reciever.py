import cv2
import sys
import os
import time

sys.path.append("/home/foscar/capstone/lib/python3.8/site-packages")

cap = cv2.VideoCapture(0)
cap.set(3, 1080)
cap.set(4, 1920)
fc = 20.0

count = 0
codec = cv2.VideoWriter_fourcc('D', 'I', 'V', 'X')
writing_video_dir="writing_video"
receive_video_dir="receive_video"

record_flag = False
init_flag = False
startTime=None
while True:
    ret, frame = cap.read()
    cv2.imshow('test', frame)
    k = cv2.waitKey(1)
    if k == 27:
        break
    if not record_flag:
        record_flag=True
        startTime=time.time()
        tm=time.gmtime(startTime)
        avi_name=startTime
        # avi_name=f"{tm.tm_year}.{tm.tm_mon}.{tm.tm_mday}.{tm.tm_hour}:{tm.tm_min}:{tm.tm_sec}"

        # a=time.strftime('%c', time.localtime(startTime))
        # out = cv2.VideoWriter(f'{count}.avi', codec, fc, (int(cap.get(3)), int(cap.get(4))))
        out = cv2.VideoWriter(f'{writing_video_dir}/{avi_name}.avi', codec, fc, (int(cap.get(3)), int(cap.get(4))))
    if startTime!=None and record_flag:
        if time.time()-startTime<5:
            out.write(frame)
        else:
            record_flag=False
            out.release()
            print(f"{avi_name} Saved")
            os.system(f"mv {writing_video_dir}/* {receive_video_dir}/")
cap.release()
cv2.destroyAllWindows()
