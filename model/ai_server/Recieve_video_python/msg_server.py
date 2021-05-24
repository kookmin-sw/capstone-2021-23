import socket
import os

import buffer

HOST = ''
PORT = 2346

s = socket.socket()
s.bind((HOST, PORT))
s.listen(10)
print("Waiting for a connection.....")


while True:
    conn, addr = s.accept()
    conn.send("a".encode());
    print('Connection closed.')
    conn.close()
