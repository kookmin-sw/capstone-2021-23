import cv2
import sys
import os
import time


cap = cv2.VideoCapture(0)
# cap.set(3, 1080)
# cap.set(4, 1920)

fc = 20.0
count = 0

codec = cv2.VideoWriter_fourcc(*"mp4v")
writing_video_dir="writing_video"
receive_video_dir="receive_video"

record_flag = False
init_flag = False
startTime=None
out = None

while True:

    ret, frame = cap.read()
    cv2.imshow('test', frame)

    k = cv2.waitKey(1)
    if k == 27:
        break

    if not record_flag:
        record_flag=True
        startTime=time.time()
        # out = cv2.VideoWriter(f'{count}.avi', codec, fc, (int(cap.get(3)), int(cap.get(4))))
        out = cv2.VideoWriter(f'{writing_video_dir}/{startTime}.mp4', codec, fc, (int(cap.get(3)), int(cap.get(4))))

    if startTime!=None and record_flag:

        if time.time()-startTime<5:
            out.write(frame)
        else:
            record_flag=False
            out.release()
            print("Saved")
            os.system(f"mv {writing_video_dir}/* {receive_video_dir}/")

cap.release()
out.release()
cv2.destroyAllWindows()
os.system(f"rm {writing_video_dir}/*")
