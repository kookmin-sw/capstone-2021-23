import os
import argparse
import os.path as osp
import requests
import torch
from collections import defaultdict
from mmaction.apis import inference_recognizer, init_recognizer
import json

server_url = "http://"+"192.168.0.15:8040"+"/users/email/"

def StrConverter(filename:str)->dict:
    key=['year','month','day','hour','min','sec']
    filename=filename.replace(".",' ')
    filename=filename.replace(":",' ')
    data={ i:j for i,j in list(zip(key,filename.split())) }
    return data
receive_path= 'receive_video/'
path_dir = 'video_for_process/'
db       = "assult_candidate/"
device = torch.device("cuda")
# build the recognizer from a config file and checkpoint file/url
config="../configs/recognition/slowfast/custom.py"
checkpoint="../data_center/fight_assault/BinaryDataTree/tanos_lr_improve_checkpoints/epoch_70.pth"
model = init_recognizer(
    config,
    checkpoint,
    device=device,
    )
label="../demo/custom_map.txt"
while True:
    if not os.listdir(receive_path):
        continue
    os.system(f"mv {receive_path}* {path_dir}")
    file_list = os.listdir(path_dir)
    file_list.sort()#시간순 정렬
    for i in file_list:
        results = inference_recognizer(model,path_dir+i,label)
        if results[0][0]=="abnormal" and results[0][1]>0.86:
            '''
            폭력 발생 db로 영상 보내야 함 and 처리 완료이므로 디렉토리에서 pop
            '''
            os.system(f"mv {path_dir+i} {db}")
            data=StrConverter(i)
            data["cam_num"]=0
            print(data)
            try:
                r = requests.post(server_url, data= json.dumps(data))
                print("post")
            except:
                print("error")
            print(f"moved to db and abnormal score : {results[0][1]}")
            #웹서버로 보내버리기

        else:
            '''
            폭력 발생 x 이므로 디렉토리에서 영상 걍 삭제
            '''
            os.system(f"rm {path_dir+i}")
            print(f"removed {path_dir+i} and :{results}")

