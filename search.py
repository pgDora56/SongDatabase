from db import *
import difflib, sys

db = DB()
alldata = db.get_all()

args = sys.argv

def command(s):
    if s.startswith("."):
        if s == ".quit":
            return False
        elif s == ".all":
            sortdata = sorted(alldata, key = lambda x: x[5], reverse = True)
            for res in sortdata:
                print("{} {} {}".format(res[2], res[3], res[4]))
                print("{} / {}".format(res[0], res[1]))
                print("Priority: {}".format(res[5]))
                print()
        elif s.startswith(".priority"):
            searchword = s.split()
            
        elif s.startswith(".year"):
            searchword = s.split()

    else:
        result = []
        for song in alldata:
            value = 0
            contain = False
            for counter in range(len(song) - 1):
                if counter == 2: continue
                d = song[counter]
                if isinstance(d, int): d2 = str(d)
                else: d2 = d
                value = max([value, difflib.SequenceMatcher(None, s, d2).ratio()])
                if s in d2:
                    contain = True
            if value > 0.5:
                result.append((value, song))
            elif contain:
                result.append((value, song))
        result.sort(key = lambda x: x[0], reverse = True)
        print("\n====> Search '{}'\n".format(s))
        for res in result:
            print("{} {} {}".format(res[1][2], res[1][3], res[1][4]))
            print("{} / {}".format(res[1][0], res[1][1]))
            print("Priority: {}".format(res[1][5]))
            print()
    return True

if __name__ == '__main__':
    if len(args) > 1:
        search_word = ""
        for i in range(1, len(args)):
            if i != 1: search_word += " "
            search_word += args[i]
        command(search_word)
    else:
        print("Anison Database Search Application version 1.0.0")
        print('Enter ".quit" if you want to quit.')

        loop = True
        while loop: 
            s = input("ADS > ")
            loop = command(s)
        print("See you.")