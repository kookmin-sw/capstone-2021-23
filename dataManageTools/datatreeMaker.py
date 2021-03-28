import random
import os

normal_path_dir = '../normal'
punching_path_dir = '../punching'
kicking_path_dir = '../kicking'
if not os.path.isdir('train'):
    os.mkdir('train')
if not os.path.isdir('val'):
    os.mkdir('val')

normal_file_list = os.listdir(normal_path_dir)
punching_file_list = os.listdir(punching_path_dir)
kicking_file_list = os.listdir(kicking_path_dir)

# print(len(normal_file_list))
# print(len(punching_file_list))
# print(len(kicking_file_list))

random.shuffle(normal_file_list)
random.shuffle(annormal_file_list)


def list_splitter(list_to_split, ratio):
    elements = len(list_to_split)
    middle = int(elements * ratio)
    return [list_to_split[:middle], list_to_split[middle:]]


# print(list)
train_normal_list,val_normal_list=list_splitter(normal_file_list,0.8)
train_punching_list,val_punching_list=list_splitter(punching_file_list,0.8)
train_kicking_list,val_kicking_list=list_splitter(kicking_file_list,0.8)

f = open("train.txt", 'w')
# f.close()
for i in train_normal_list:
    f.write(f"normal{i} 0\n")
    os.system(f"cp {normal_path_dir}/{i} train/normal{i}")

for i in train_punching_list:
    f.write(f"punching{i} 1\n")
    os.system(f"cp {punching_path_dir}/{i} train/punching{i}")

for i in train_kicking_list:
    f.write(f"kicking{i} 2\n")
    os.system(f"cp {kicking_path_dir}/{i} train/kicking{i}")

f.close()

f = open("val.txt", 'w')
for i in val_normal_list:
    f.write(f"normal{i} 0\n")
    os.system(f"cp {normal_path_dir}/{i} val/normal{i}")

for i in val_punching_list:
    f.write(f"punching{i} 1\n")
    os.system(f"cp {punching_path_dir}/{i} val/punching{i}")

for i in val_kicking_list:
    f.write(f"kicking{i} 2\n")
    os.system(f"cp {kicking_path_dir}/{i} val/kicking{i}")

f.close()
# f.close()
# print(train_normal_list)
# for i in range()


# # 출처: https://icodebroker.tistory.com/4299 [ICODEBROKER]
# print(normal_file_list)
# print(annormal_file_list)
