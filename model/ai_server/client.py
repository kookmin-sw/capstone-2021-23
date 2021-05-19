import socket
import threading
import os
import cv2
import numpy as np
from humanDetect import isPeople
import buffer

HOST = '127.0.0.1'
PORT = 2345

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect((HOST, PORT))


path = './receive_video/'

while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    with s:
#!/usr/bin/python3
from socket import socket, gethostname, SHUT_WR
import os
s = socket()
host = gethostname()
port = 3399
s.connect((host, port))
path="assult_candidate"
for i in os.listdir(path):
    print("Sending video..")
    with open(f"{path}/{i}", "rb") as video:
        buffer = video.read()
        print(buffer)
        s.sendall(buffer)
        print("Done sending..")
    s.close()


        while True:
            files_to_send = os.listdir(path)

            if len(files_to_send) >= 1:
                break
            else:
                continue


        sbuf = buffer.Buffer(s)

        hash_type = 'a'


        for file_name in files_to_send:
            print(file_name)
            sbuf.put_utf8(hash_type)
            sbuf.put_utf8(file_name)

            file_size = os.path.getsize(path + file_name)
            sbuf.put_utf8(str(file_size))
            cap=cv2.VideoCapture(path+file_name)
            ret,frame=cap.read()
            cv2.imshow("q",frame)
            cv2.waitKey(1)
            if not isPeople(frame): continue
            with open(path + file_name, 'rb') as f:

                img_str=f.read()
                sbuf.put_bytes(img_str)
            print('File Sent')
        os.system(f"rm ./receive_video/*.mp4")
