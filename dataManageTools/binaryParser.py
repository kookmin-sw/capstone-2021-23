from xml.etree.ElementTree import parse
import os
# import cv2
import os, sys
import argparse
parser = argparse.ArgumentParser(description='input name')
parser.add_argument('--name', type=str,
                    help='mp4 name')
args= parser.parse_args()
# print(name.name)
# parser.add_argument('--sum', dest='accumulate', action='store_const',
#                     const=sum, default=max,
#                     help='sum the integers (default: find the max)')
tree = parse('./'+args.name+'.xml')
root = tree.getroot()
path='./'
object = root.findall("object")
FRAME=30

action_frame={}
constKey='annormal'
action_frame[constKey]=[]
if not os.path.isdir(path+"normal"):
    os.mkdir(path+"normal")
if not os.path.isdir(path+"annormal"):
    os.mkdir(path+"annormal")

for i in object:
    for j in i.findall("action"):
        temp=j.find("actionname").text
        if temp!='punching' and temp!='kicking':
            continue
        for x in j.findall("frame"):
            action_frame[constKey].append((int(x.find('start').text),int(x.find('end').text)))
if len(action_frame[constKey])==0:
    print("no action")
    sys.exit()
pre_processed_action_frame={}
for i in list(action_frame.keys()):
    start=0
    end=0
    pre_processed_action_frame[i]=[]
    for j in action_frame[i]:
        if j[0]-end>15 or (start<=0 and end<=0):
            if start>0 and end>0:
                pre_processed_action_frame[i].append((start,end))
            start,end=j
        else:
            end=j[1]
    pre_processed_action_frame[i].append((start-15,end+15))
# print(pre_processed_action_frame)

def humanize_time(secs):
    mins, secs = divmod(secs, 60)
    hours, mins = divmod(mins, 60)
    return '%02d:%02d:%02d' % (hours, mins, secs)
input=args.name+".mp4"
cnt=0
# print(pre_processed_action_frame)
# if not os.path.isfile(path+f"small_{input}"):
#     NEWCODE= f"ffmpeg -i {input} -s 960x540 -strict -2  -profile:v main small_{input} > /dev/null"
#     os.system(NEWCODE)
tempEnd=pre_processed_action_frame[constKey][0][0]/3
import random
cnt=0
# for i in range(1,tempEnd-200,random.randint(90,180)):
i=1
while i<tempEnd:
    cnt+=1
    starttime=humanize_time(i//FRAME)
    a=random.randint(90,180)
    endtime=humanize_time((i+a)//FRAME)
    NEWCODE= f"ffmpeg -i {input} -strict -2 -ss {starttime} -to {endtime} ./normal/{args.name}{i}.mp4"
    os.system(NEWCODE)
    i+=a
for i in pre_processed_action_frame.keys():
    cnt=0
    action_name=i
    # print(action_name)
    for start,end in pre_processed_action_frame[i]:
        starttime=humanize_time(start//FRAME)
        endtime=humanize_time(end//FRAME)


        if end-start>=64:
            cnt+=1
            # if not os.path.isfile(path+f"{action_name}/{args.name+str(cnt)}.mp4"):
            NEWCODE= f"ffmpeg -i {input} -strict -2 -ss {starttime} -to {endtime} ./{action_name}/{args.name+str(cnt)}.mp4"
            os.system(NEWCODE)
            # NEWCODE= f"ffmpeg -i {action_name}/{args.name+str(cnt)}.mp4 -s 960x540 -strict -2  -profile:v main small_{action_name}/small_annormal{args.name+str(cnt)}.mp4"
            # os.system(NEWCODE)
            # NEWCODE= f"rm ./annormal/{args.name}{i}.mp4"
            # os.system(NEWCODE)

