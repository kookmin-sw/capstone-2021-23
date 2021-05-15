import os
import argparse
import os.path as osp

import torch

from mmaction.apis import inference_recognizer, init_recognizer

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
            print(f"moved to db and abnormal score : {results[0][1]}")

        else:
            '''
            폭력 발생 x 이므로 디렉토리에서 영상 걍 삭제
            '''
            os.system(f"rm {path_dir+i}")
            print(f"removed {path_dir+i} and :{results}")

