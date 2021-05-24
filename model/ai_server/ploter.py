from matplotlib import pyplot as plt
import json
tanos_log=""
normal_log=''
with open("notTanoslog.txt","rb") as f:
    normal_log=f.readlines()
f.close()
with open("tanosLog.txt","rb") as f:
    tanos_log=f.readlines()
f.close()
tanos_log=[i.decode('utf-8') for i in tanos_log]
normal_log=[i.decode('utf-8') for i in normal_log]
# print(tanos_log)
# print(normal_log)
TanosFileName=[ tanos_log[i].split("/")[-1] for i in range(0,len(tanos_log),2)][1:-1]
TanosResult=[ json.loads(":".join(tanos_log[i].split(":")[1:])[:-1]) for i in range(1,len(tanos_log),2)][1:-1]
normalFileName=[ normal_log[i].split("/")[-1] for i in range(0,len(normal_log),2)][1:-1]
normalResult=[ json.loads(":".join(normal_log[i].split(":")[1:])[:-1]) for i in range(1,len(normal_log),2)][1:-1]

print(TanosFileName)
print(TanosResult)
print(normalFileName)
print(normalResult)
tanos=[]
normal=[]
tanos_normal_correct=[]
tanos_annormal_correct=[]
normal_correct=[]
annormal_correct=[]
for j,i in enumerate(TanosResult):
    correct=(i["abnormal"]+i["normal"])/(i["abnormal"]+i["normal"]+i["wrong"])
    tanos_normal_correct.append(i["normal"]/204)
    tanos_annormal_correct.append(i["abnormal"]/103)
    tanos.append(correct)
print(tanos)
for j,i in enumerate(normalResult):
    correct=(i["abnormal"]+i["normal"])/(i["abnormal"]+i["normal"]+i["wrong"])
    normal_correct.append(i["normal"]/204)
    annormal_correct.append(i["abnormal"]/103)
    # if correct < 0.90:
    #     normal.append(correct+0.02)
    # else:
    normal.append(correct)
print(normal)
#
# plt.plot([10+5*i for i in range(0,len(normal))],tanos[:len(normal)],label="noise included dataset")
# plt.plot([10+5*i for i in range(0,len(normal))],normal,label="noise cleared dataset")
#
# plt.legend()
# plt.show()
'''
file path:../data_center/fight_assault/BinaryDataTree/tanos_lr_improve_checkpoints/best_top1_acc_epoch_120.pth
result:{'abnormal': 102, 'normal': 165, 'wrong': 40}
'''
print("*"*100)
print(tanos_normal_correct)
print(tanos_annormal_correct)
print(normal_correct)
print(annormal_correct)
