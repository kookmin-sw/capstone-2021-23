import os
import random

if not os.path.isdir('test_normal'):
    os.mkdir('test_normal')
if not os.path.isdir('test_punching'):
    os.mkdir('test_punching')
if not os.path.isdir('test_kicking'):
    os.mkdir('test_kicking')

path_dir="../2021_capstone/mmaction2/data_center/fight_assault"
normal_path=path_dir+"/normal"
kicking_path=path_dir+"/kicking"
punching_path=path_dir+"/punching"
normal_file_list = os.listdir(normal_path)
kicking_file_list = os.listdir(kicking_path)
punching_file_list = os.listdir(punching_path)

random.shuffle(normal_file_list)
random.shuffle(kicking_file_list)
random.shuffle(punching_file_list)
# print(normal_file_list[0].find("fight"))
normal_test_candidate=[i for i in normal_file_list if "fight" in i ]
punching_test_candidate=[i for i in punching_file_list if "fight" in i ]
kicking_test_candidate=[i for i in kicking_file_list if "fight" in i ]

# print(len(normal_test_candidate))
# print(len(punching_test_candidate))
# print(len(kicking_test_candidate))

normal_test_candidate=normal_test_candidate[:481]
kicking_test_candidate=kicking_test_candidate[:481]
punching_test_candidate=punching_test_candidate[:481]

print(len(normal_test_candidate))
print(len(punching_test_candidate))
print(len(kicking_test_candidate))

for i in normal_test_candidate:
    os.system(f"cp {normal_path}/{i} test_normal/{i}")
for i in kicking_test_candidate:
    os.system(f"cp {kicking_path}/{i} test_kicking/{i}")
for i in punching_test_candidate:
    os.system(f"cp {punching_path}/{i} test_punching/{i}")
# for i in normal_test_candidate:

# print(len(punching_test_candidate))
# print(kicking_file_list)
# print(punching_file_list)
