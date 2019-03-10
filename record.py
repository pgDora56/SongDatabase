# coding: utf-8

import sys, sqlite3, difflib
from db import DB

args = sys.argv
db = DB()
judge_datas = db.get_judge()

if len(args) > 1:
    for i in range(1, len(args)):
        with open(args[i], 'r', encoding = 'utf-8') as f:
            while True:
                try:
                    d = f.readline()
                    if d == "\n":
                        continue
                    if d.startswith('#ignore') : break
                    if d.startswith('#') : continue
                    data = d.rstrip('\n').split('|')
                    types = data[1].split()
                    tp = ""
                    yr = -1
                    for t in types:
                        if t.isdigit():
                            yr = int(t)
                            break
                        else:
                            tp += t
                    db.insert((data[3], data[4], yr, tp ,data[0]))
                    # entry = False
                    # for song in judge_datas:
                    #     ratio = difflib.SequenceMatcher(None, song[0], data[3]).ratio()
                    #     if ratio >= 0.75:
                    #         c = ""
                    #         if ratio == 1.0: c = "T"
                    #         else:
                    #             print("☆以下の2データは同じデータですか？")
                    #             print("● {} / {}".format(song[0], song[1]))
                    #             print("● {} / {}".format(data[3], data[4]))
                    #         while not c in ["T", "t", "F", "f"]:
                    #             c = input("T/F > ")
                    #         if c in ["T", "t"]:
                    #             db.cursor.execute("UPDATE songs SET priority = priority + 1 WHERE title = ? AND artist = ?", (data[3], data[4]))
                    #             db.write()
                    #             print('{} / {} => Priority Up'.format(data[3], data[4]))
                    #             entry = True
                    #             break
                    # if not entry:
                    #     db.cursor.execute("INSERT INTO songs(title, artist, year, type, animetitle) VALUES(?, ?, ?, ?, ?)", (data[3], data[4], yr, tp ,data[0]))
                    #     db.write()
                    #     print('{} / {} => Add'.format(data[3], data[4]))
                    #     judge_datas.append((data[3], data[4]))
                        
                    # songdata.append((data[3], data[4], yr, tp ,data[0]))
                except EOFError:
                    break
                except IndexError:
                    break
                except:
                    print("Throw error in {}".format(args[i]))
                    import traceback
                    traceback.print_exc()
                    exit()
else:
    print("Anison Database Record Application version 1.0.0")
    print('Enter ".quit" if you want to quit.')
    while True: 
        i = input("ADR > ")
        if i.startswith(".quit"):
            break
        datas = i.split('|')
        com = ""
        if len(datas) == 3:
            com = datas[2]
        elif len(datas) != 2:
            continue
        db.insert((datas[0], datas[1], com))
    print("See you.")
db.wq()
# print(songdata)
