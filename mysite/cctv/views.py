from django.views.decorators import gzip
from django.http import StreamingHttpResponse
import cv2
import threading
from django.shortcuts import render

#첫 회원가입시 감시할 cctv선택할 html 페이지로 rendering할 라이브러리
from django.template import loader
from django.db.models import Count
from django.http import HttpResponse
#cctv model에서 사용가능한(is_used=False)인 cctv수 count
from .models import Cctv

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(
    'udpsrc port=8051 caps = "application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)H264"'
    ' ! rtph264depay'
    ' ! avdec_h264'
    ' ! videoconvert'
    ' ! appsink', cv2.CAP_GSTREAMER)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        _, jpeg = cv2.imencode('.png', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@gzip.gzip_page
def serveStreaming(request):
    try:
        cam = VideoCamera()
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:  # This is bad! replace it with proper handling
        pass

def index(request):
    return render(request, 'cctv/index.html')

def select_cctv(request):
    available_cctv = Cctv.objects.filter(is_used=False)
    print(available_cctv)
    template = loader.get_template('cctv/select_cctv.html')
    context ={
        'num_available_cctv': available_cctv.count(),
        'cctvs' : available_cctv,
    }
    return HttpResponse(template.render(context, request))
   # return render(request, 'cctv/select_cctv.html')
