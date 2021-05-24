from django.views.decorators import gzip
from django.http import StreamingHttpResponse
import cv2
import threading
from django.shortcuts import render,redirect,reverse


from django.template import loader
from django.db.models import Count
from django.http import HttpResponse
from .models import Cctv
import os
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from .models import Record

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(
    'udpsrc port=8061 caps = "application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)H264"'
    ' ! rtpjitterbuffer'
    ' ! rtph264depay'
    ' ! h264parse'
    ' ! avdec_h264'
    ' ! decodebin'
    ' ! videoconvert'
    ' ! appsink emit-signals=true sync=false max-buffers=2 drop=true', cv2.CAP_GSTREAMER)
        #self.video = cv2.VideoCapture("udpsrc port=8061 ! application/x-rtp-stream,encoding-name=JPEG ! rtpstreamdepay ! rtpjpegdepay ! jpegdec ! videoconvert ! appsink emit-signals=true sync=false max-buffers=2 drop-true", cv2.CAP_GSTREAMER)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        ret, jpeg = cv2.imencode('.png', image)
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
        #cam = VideoCamera()
        return StreamingHttpResponse(gen(VideoCamera()), content_type="multipart/x-mixed-replace;boundary=frame")
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
   

def main_page(request):
    template = loader.get_template('cctv/main.html')
    dir = "/home/capstone/capstone-2021-23/mysite/data/assult_candidate/"
    file_list = sorted(os.listdir(dir),reverse= True)
    
    date_list = []
    for file in file_list:
        time_info = file.split('_')
        sec_info = time_info[5].split('.')
        name = f'{time_info[0]}년 {time_info[1]}월 {time_info[2]}일 {time_info[3]}시 {time_info[4]}분 {sec_info[0]}초 '
        date_list.append(name)
    
    records = Record.objects.last()
    dir_path ="http://58.142.223.232:8080/assult_candidate/"
    
    if records is None:
        for file_name,record in zip(file_list, date_list):
            record  = Record.objects.create(
                file_path = dir_path+file_name,
                record_date = record
            )
            
            record.save()
    
    
    
    file_record_info = Record.objects.all
    context ={
        'infos' : file_record_info
    }
    return HttpResponse(template.render(context, request))

@csrf_exempt
def save_cctv(request):
    #print(json.loads(request.body.decode('utf-8')))
    #orm = NameForm(request.POST)
    cam_loc = request.POST["submit"]
    #am = Cctv.objects.get(
    #       user_account.save()

    return redirect('cctv:main_page')
