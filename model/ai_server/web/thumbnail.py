#-*- encoding: utf-8 -*-. -

import cv2


def make_thumbnail(file_name):
    video_dir = "/home/foscar/Desktop/2021_capstone/mmaction2/ai_server/web/assult_candidate/"
    thumbnail_dir = "/home/foscar/Desktop/2021_capstone/mmaction2/ai_server/web/thumbnail/"

    cap = cv2.VideoCapture(video_dir + file_name)
    count = 0

    while True:
        ret,frame = cap.read()

        if not ret:
            print("can not read video")

        if count > 50:
            cv2.imwrite(f"{thumbnail_dir + file_name.split('.')[0]}.jpg", frame)
            break

        count += 1

    return f"{file_name.split('.')[0]}.jpg"

if __name__ == "__main__":
    make_thumbnail("a.mp4")
