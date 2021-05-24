import os
import argparse
import os.path as osp
import requests
import torch
from collections import defaultdict
from mmaction.apis import inference_recognizer, init_recognizer
import json
from io import StringIO

def return_print(*message):
    io = StringIO()
    print(*message, file=io, end="")
    return io.getvalue()

# wow = return_print("하하", "호호", "히히")
# server_url = "http://"+"192.168.0.15:8040"+"/users/email/"
#r = requests.post("http://"+"192.168.0.15:8040"+"/users/email/")

def StrConverter(filename:str)->dict:

    key=['year','month','day','hour','min','sec']
    filename=filename.replace(".",' ')
    filename=filename.replace(":",' ')
    data={ i:j for i,j in list(zip(key,filename.split())) }
    return data
# THRESEHOLD=(0.56)
device = torch.device("cuda")
config="../configs/recognition/slowfast/custom.py"
'''

35 주석풀고 37 주석

'''
checkpoint="../data_center/fight_assault/BinaryDataTree/tanos_lr_improve_checkpoints/"

# checkpoint="../data_center/fight_assault/BinaryDataTree/lr_improve_checkpoints/"
pth_list=sorted([ i for i in os.listdir(checkpoint) if i.endswith(".pth")])

# pth_list.sort()
label="../demo/custom_map.txt"

path_dir = ['abnormal','normal']
# with open("acc_check_log.txt", 'w') as f:
#     # a=eval(print(path_dir))
#     f.write(return_print(path_dir))
# build the recognizer from a config file and checkpoint file/url

'''
53주석풀고 54 주석
'''

with open("tanos_acc_check_log.txt", 'w') as f:
# with open("acc_check_log.txt", 'w') as f:
    for i in pth_list:
        pth_path=checkpoint+i
        print(pth_path)
        print("@"*50)
        model = init_recognizer(
        config,
        pth_path,
        device=device
        )
        total=0
        correct={"abnormal":0,"normal":0,"wrong":0}
        for path in path_dir:                # data["day"] = "2021년 5월 22일"
                # data["time"] = "15시 30분"
            # print(f"pth file: {i}",end=" ")
            file_list = os.listdir(path)
            total+=len(file_list)
            file_list.sort()#시간순 -p 10000:10000/udp정렬
            for j,i in enumerate(file_list):
                print(f"now {path} inference and total count:{j}",end=" ")
                results=inference_recognizer(model,path+"/"+i,label)
                if path==results[0][0]:# with open("acc_check_log.txt", 'w') as f:
#     # a=eval(print(path_dir))
#     f.write(return_print(path_dir))
                    correct[path]+=1
                    print(f"correct: {correct} ")
                else:
                    correct["wrong"]+=1
                    print(f"WRONG!! correct: {correct} ")
        fileName_log="file path:"+return_print(pth_path)+"\n"
        result_log="result:"+return_print(f"{correct}")+"\n"
        f.write(fileName_log)
        f.write(result_log)
        print(fileName_log)
        print(result_log)
        # f.write(return_print(f"pth path: {pth_path}"))
        # f.write(return_print("/".join(checkpoint.split("/")[-2:])))
        # print(return_print(f"{correct}"))
        # print(return_print("/".join(checkpoint.split("/")[-2:])))
        # f.write(return_print(correct))
        # f.write(return_print(total))
        # print("/".join(checkpoint.split("/")[-2:]))
        # print(results)
        # print(correct)
        # print(total)
        # print(correct/total)
f.close()
