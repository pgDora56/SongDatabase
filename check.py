from db import * 
import difflib

db = DB()
judge_datas = db.get_judge()
nm = len(judge_datas)
ratio_data = []
for i in range(nm - 1):
    for j in range(i + 1, nm):
        ratio_data.append((judge_datas[i][1], judge_datas[j][1], difflib.SequenceMatcher(None, judge_datas[i][1], judge_datas[j][1]).ratio()))

for i in ratio_data:
    if(1 > i[2] > 0.5):
        print(i)

