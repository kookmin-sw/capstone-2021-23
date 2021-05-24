import os

filelist = os.listdir('./assult_candidate')

print(filelist)


for file in filelist:
    os.system(f'ffmpeg -i ./assult_candidate/{file} -vcodec libx264 -acodec aac ./process/{file}')


#2135 1907 
