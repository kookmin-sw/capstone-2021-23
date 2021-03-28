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
print(object)
action_frame={}
constKey1='punching'
constKey2='kicking'

if not os.path.isdir(path+"normal"):
    os.mkdir(path+"normal")

for i in object:
    for j in i.findall("action"):
        temp=j.find("actionname").text
        if temp not in action_frame.keys() and temp==constKey1 or temp==constKey2:
            action_frame[temp]=[]
        if temp==constKey1:
            if not os.path.isdir(path+temp):
                    os.mkdir(path+temp)
            for x in j.findall("frame"):
                action_frame[temp].append((int(x.find('start').text),int(x.find('end').text)))
        if temp==constKey2:
            if not os.path.isdir(path+temp):
                    os.mkdir(path+temp)
            for x in j.findall("frame"):
                action_frame[temp].append((int(x.find('start').text),int(x.find('end').text)))
        else:
            continue
        # print(temp)



        # for x in j.findall("frame"):
        #     action_frame[temp].append((int(x.find('start').text),int(x.find('end').text)))



# for i in list(action_frame.keys()):
#     if len(action_frame[i])==0:
#         del action_frame[i]
# print(action_frame)
tempEnd=0

# '''
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
    pre_processed_action_frame[i].append((start-10,end+10))

if constKey1 not in action_frame.keys() and constKey2 not in action_frame.keys():
    print("no dangerous")
    sys.exit()
elif constKey2 not in action_frame.keys():
    tempEnd=pre_processed_action_frame[constKey1][0][0]/3
elif constKey1 not in action_frame.keys():
    tempEnd=pre_processed_action_frame[constKey2][0][0]/3
else:
    tempEnd=min(pre_processed_action_frame[constKey2][0][0]/3,pre_processed_action_frame[constKey1][0][0]/3)
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
#     os.system(NEWCODE)                    os.mkdir(path+"normal")



import random
cnt=0

# for i in range(1,tempEnd-200,random.randint(90,180)):
i=1
while i<tempEnd:
    cnt+=1
    starttime=humanize_time(i//FRAME)
    a=random.randint(90,180)
    endtime=humanize_time((i+a)//FRAME)

    NEWCODE= f"ffmpeg -i {input} -strict -2 -ss {starttime}.0 -to {endtime}.0 ./normal/{args.name}{cnt}.mp4"
    os.system(NEWCODE)
    # NEWCODE= f"ffmpeg -i ./normal/{args.name}{i}.mp4 -s 960x540 -strict -2  -profile:v main small_normal/small_normal{args.name}{cnt}.mp4"
    # os.system(NEWCODE)
    # NEWCODE= f"rm ./normal/{args.name}{i}.mp4"
    # os.system(NEWCODE)
    i+=a
for i in pre_processed_action_frame.keys():
    cnt=0
    action_name=i
    # print(action_name)
    for start,end in pre_processed_action_frame[i]:
        starttime=humanize_time(start//FRAME)
        endtime=humanize_time(end//FRAME)
        # print("start: ",starttime)
        # print("end  : ",endtime)

        if end-start>=64 :
            cnt+=1
            # if not os.path.isfile(path+f"{action_name}/{args.name+str(cnt)}.mp4"):
            NEWCODE= f"ffmpeg -i {input} -strict -2 -ss {starttime} -to {endtime} ./{action_name}/{args.name+str(cnt)}.mp4"
            os.system(NEWCODE)
            # NEWCODE= f"ffmpeg -i {action_name}/{args.name+str(cnt)}.mp4 -s 960x540 -strict -2  -profile:v main small_{action_name}/small_{action_name}{args.name+str(cnt)}.mp4"
            # os.system(NEWCODE)
            # NEWCODE= f"rm ./{i}/{args.name+str(cnt)}.mp4"
            # os.system(NEWCODE)
