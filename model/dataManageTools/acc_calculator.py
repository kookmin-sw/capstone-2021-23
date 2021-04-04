from mmaction.apis import inference_recognizer, init_recognizer
import os
# Choose to use a config and initialize the recognizer
config = '/home/workspace/2021_capstone/mmaction2/configs/recognition/slowfast/custom.py'
# Setup a checkpoint file to load
checkpoint = '/home/workspace/2021_capstone/mmaction2/data_center/assult/best_top1_acc_epoch_185.pth'
# Initialize the recognizer
model = init_recognizer(config, checkpoint, device='cuda:0')
# path_dir="../2021_capstone/mmaction2/data_center/fight_assault"
path_dir='.'
# path_dir="../2021_capstone/mmaction2/data_center/fight_assault"
normal_path=path_dir+"/test_normal"
kicking_path=path_dir+"/test_kicking"
punching_path=path_dir+"/test_punching"
normal_file_list = os.listdir(normal_path)
kicking_file_list = os.listdir(kicking_path)
punching_file_list = os.listdir(punching_path)
label = '/home/workspace/2021_capstone/mmaction2/demo/custom_map.txt'

dir=[kicking_file_list,normal_file_list,punching_file_list]

total_testSet=0

for i in dir:
    total_testSet+=len(i)

kicking_cnt=0
punching_cnt=0
normal_cnt=0
iter=0
for i in dir:
    iter=0
    # print(i)
    for j in i:

        # print(f"Now {i} dir and {iter} frames",end=" ")
        iter+=1
        if i==normal_file_list:
            print(f"Now normal dir and {iter} frames",end=" ")

            results = inference_recognizer(model,normal_path+"/"+j, label)
            # print(results[0][0])
            if results[0][0]=='normal':
                normal_cnt+=1
                print(f'correct : {normal_cnt} {normal_cnt/iter}')
            else:
                print(f"NOPE : {normal_cnt} {normal_cnt/iter}")
        elif i==kicking_file_list:
            print(f"Now kick dir and {iter} frames",end=" ")

            results = inference_recognizer(model,kicking_path+"/"+j, label)
            # print(results[0][0])
            if results[0][0]=='kick':
                kicking_cnt+=1
                print(f'correct : {kicking_cnt} {kicking_cnt/iter}')
            else:
                print(f'Nope : {kicking_cnt} {kicking_cnt/iter}')
        elif i==punching_file_list:
            print(f"Now punch dir and {iter} frames",end=" ")

            results = inference_recognizer(model,punching_path+"/"+j, label)
            # print(results[0][0])
            if results[0][0]=='punch':
                punching_cnt+=1
                print(f'correct : {punching_cnt} {punching_cnt/iter}')
            else:
                print(f'NOPE : {punching_cnt} {punching_cnt/iter}')

print(f"kicking: {kicking_cnt/len(kicking_file_list)}")
print(f"punching: {punching_cnt/len(punching_file_list)}")
print(f"normal: {normal_cnt/len(normal_file_list)}")
print(f"total: {(kicking_cnt+punching_cnt+normal_cnt)/len(total_testSet)}")

# {punching_cnt} {normal_cnt}")
