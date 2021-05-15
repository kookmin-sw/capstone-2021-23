#!/usr/bin/python3
from socket import socket, gethostname
s = socket()
host = gethostname()
port = 3399
s.bind((host, port))
s.listen(5)
n = 0
while True:
    print("Listening for connections...")
    connection, addr = s.accept()
    try:
        print("Starting to read bytes..")
        buffer = connection.recv(1024)
        with open('video_'+str(n)+'.mp4', "wb") as video:
            n += 1
            i = 0
            while buffer:
                video.write(buffer)
                print("buffer {0}".format(i))
                i += 1
                buffer = connection.recv(1024)
        print("Done reading bytes..")
        connection.close()
    except KeyboardInterrupt:
        if connection:
            connection.close()
        break
s.close()
 

