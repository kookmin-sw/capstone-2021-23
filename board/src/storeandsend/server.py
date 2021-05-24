import socket
import os

import buffer

HOST = ''
PORT = 2345

# If server and client run in same local directory,
# need a separate place to store the uploads.
try:
    os.mkdir('uploads')
except FileExistsError:
    pass

s = socket.socket()
s.bind((HOST, PORT))
s.listen(10)
print("Waiting for a connection.....")

while True:
    conn, addr = s.accept()
    print("Got a connection from ", addr)
    connbuf = buffer.Buffer(conn)

    while True:
        hash_type = connbuf.get_utf8()
        if not hash_type:
            break
        print('hash type: ', hash_type)

        file_name = connbuf.get_utf8()
        if not file_name:
            break
        file_name = os.path.join('uploads',file_name)
        print('file name: ', file_name)

        file_size = int(connbuf.get_utf8())
        print('file size: ', file_size )

        with open(file_name, 'wb') as f:
            remaining = file_size
            while remaining:
                chunk_size = 4096 if remaining >= 4096 else remaining
                chunk = connbuf.get_bytes(chunk_size)
                if not chunk: break
                f.write(chunk)
                remaining -= len(chunk)
            if remaining:
                print('File incomplete.  Missing',remaining,'bytes.')
            else:
                print('File received successfully.')
    print('Connection closed.')
    conn.close()
