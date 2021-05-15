from django.views.decorators import gzip
from django.shortcuts import render
from django.http import HttpResponse
from django.http import StreamingHttpResponse
#from camera import VideoCamera

# Create your views here.

def index(request):
    return render(request,'cctv/index.html')

import cv2

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
ds_factor = 0.6


class VideoCamera(object):
    def __init__(self):
        print('gen cam')
        self.video = cv2.VideoCapture(
            'udpsrc port=8001 caps = "application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)H264, payload=(int)96" ! rtpjitterbuffer ! rtph264depay ! decodebin  ! videoconvert ! appsink',
            cv2.CAP_GSTREAMER)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        image = cv2.resize(image, None, fx=ds_factor, fy=ds_factor, interpolation=cv2.INTER_AREA)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        face_rects = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in face_rects:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            break
        ret, jpeg = cv2.imencode('.jpg', image)
        cv2.imshow(jpeg)
        cv2.waitkey(1000)
        return jpeg.tobytes()


def video_feed(request):
    print('video feed')
    return StreamingHttpResponse(gen(VideoCamera()), content_type="multipart/x-mixed-replace;boundary=frame")
    #return HttpResponse(gen(VideoCamera()),
    #                    headers={'Content-Type': 'multipart/x-mixed-replace; boundary=frame'})
                   # mimetype='multipart/x-mixed-replace; boundary=frame')

#def video_feed(request):
#    return HttpResponse('heelo')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        
