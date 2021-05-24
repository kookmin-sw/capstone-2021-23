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
