import os
import argparse
import os.path as osp
import requests
import torch
from collections import defaultdict
from mmaction.apis import inference_recognizer, init_recognizer
import json

server_url = "http://"+"192.168.0.15:8050"+"/users/email/"
#r = requests.post("http://"+"192.168.0.15:8040"+"/users/email/")

def StrConverter(filename:str)->dict:
    filename_temp=filename
    key=['year','month','day','hour','min','sec']
    filename_temp=filename_temp.replace(".",' ')
    filename_temp=filename_temp.replace(":",' ')
    time={ i:j for i,j in list(zip(key,filename_temp.split())) }
    curDay=f"{time['year']}년 {time['month']}월 {time['day']}일"
    curTime=f"{time['hour']}시 {time['min']}분"
    data=dict()
    data["filename"]=filename
    data["day"]=curDay
    data["time"]=curTime
    data["cam_num"]=0
    data["space"] = "국민대 미래관 609호"
    return data

THRESEHOLD=(0.7)
receive_path= 'receive_video/'
path_dir = 'video_for_process/'
db       = "assult_candidate/"
device = torch.device("cuda")
# build the recognizer from a config file and checkpoint file/url
config="../configs/recognition/slowfast/custom.py"
# checkpoint="../data_center/fight_assault/BinaryDataTree/tanos_lr_improve_checkpoints/epoch_60.pth"
checkpoint="../data_center/fight_assault/BinaryDataTree/lr_improve_checkpoints/epoch_55.pth"

model = init_recognizer(
    config,
    checkpoint,
    device=device,
    )
label="../demo/custom_map.txt"
os.system(f"rm -rf {path_dir}*")
os.system(f"rm -rf {receive_path}*")
while True:
    try:
        if not os.listdir(receive_path):
            continue
        os.system(f"mv {receive_path}* {path_dir}")
        file_list = os.listdir(path_dir)
        file_list.sort()#시간순 정렬
        for i in file_list:
            results = inference_recognizer(model,path_dir+i,label)
            if results[0][0]=="abnormal" and results[0][1]>THRESEHOLD:
                # os.system('./notice.sh')
                #@os.system("nvlc stop.mp3")

                #폭력 발생 db로 영상 보내야 함 and 처리 완료이므로 디렉토리에서 pop

                # cap=cv2.VideoCapture(path_dir+i)
                # ret,frame=cap.read()
                # cv2.imwrite(f'{i}.jpg',frame)
                os.system(f"mv {path_dir+i} {db}")
                data=StrConverter(i)
                # data["day"] = "2021년 5월 22일"
                # data["time"] = "15시 30분"
                ############

                # data["humb_nail"]=open(f'{i}.jpg', 'rb')
                # os.system(f"rm {i}.jpg")
                print(data)
                try:
                    r = requests.post("http://"+"192.168.0.15:8060"+"/users/email/",data = json.dumps(data))
                    # r = requests.post(server_url, data= json.dumps(data))
                    print("**************************post*********************************")
                except:
                    print("**************************server Receive error******************")
                print(f"moved to db and abnormal score : {results[0][1]}")
                #웹서버로 보내버리기

            else:

                #폭력 발생 x 이므로 디렉토리에서 영상 걍 삭제

                os.system(f"rm {path_dir+i}")
                print(f"removed {path_dir+i} and :{results}")
    except:
        print("there's noise in path_dir or receive_path")
        os.system(f"rm -rf {path_dir}*")
        os.system(f"rm -rf {receive_path}*")
