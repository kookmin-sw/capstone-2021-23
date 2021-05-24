import socket
import os
import buffer
import cv2
HOST = ''
PORT = 2345

# If server and client run in same local directory,
# need a separate place to store the uploads.
writing_video_dir="uploads"
receive_video_dir="../receive_video"
try:
    os.mkdir('uploads')
except FileExistsError:
    pass

def make_thumbnail(file_name):
    video_dir = "/home/foscar/Desktop/2021_capstone/mmaction2/ai_server/receive_video/"
    thumbnail_dir = "/home/foscar/Desktop/2021_capstone/mmaction2/ai_server/web/thumbnail/"

    # print("file name check")
    # print(file_name)
    # print(video_dir + file_name)
    cap = cv2.VideoCapture(video_dir + file_name)
    count = 0

    # print("in")
    while True:
        ret,frame = cap.read()

        if not ret:
            print("can not read video")

        if count > 50:
            # print("critical_section_in")
            cv2.imwrite(f"{thumbnail_dir + file_name.split('.')[0]}.jpg", frame)
            # print("critical_section_out")
            break

        count += 1
    # print("out")

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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
        only_file_name=file_name
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
                os.system(f"mv {writing_video_dir}/* {receive_video_dir}/")
                print('File received successfully.')

        make_thumbnail(only_file_name)

    print('Connection closed.')
    conn.close()
