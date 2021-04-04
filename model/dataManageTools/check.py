import os

path_dir = './'

file_list = os.listdir(path_dir)
new=[i.split('.')[0]  for i in file_list]
new.sort()
a=dict()
for i in new:
    if i not in a.keys():
        a[i]=1
    else:
        a[i]+=1
print(a)
remove_list=[]
for i in a.keys():
    if a[i]==1:
        remove_list.append(i)
remove_list.pop()
for i in remove_list:
    if i!='check':
        os.system(f"rm {i}*")




