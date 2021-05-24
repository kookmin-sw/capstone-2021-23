import socket
import threading
import os
from playsound import playsound
import buffer

# HOST = '127.0.0.1'
#HOST = '192.168.0.18'
HOST = '58.142.223.232'
PORT = 10000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

while True:

    dataFromServer = s.recv(1024)
    # Print to the console
    print(dataFromServer.decode('utf-8'))
    
    # annormal message check
    if dataFromServer.decode().startswith('annormal'):
        playsound('./stop.mp3')
