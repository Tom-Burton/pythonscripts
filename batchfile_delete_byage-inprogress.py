import os
import re
import time

TimeMod = input("search for files modified before: ")
print ("looking for files modified before: ",TimeMod)

DirPath = os.getcwd()
print("current directory is : " + DirPath)

DirOk = get_cmd_input("is current directory ok? (y/n)","y","n")
if DirOk == 'y':
    UseDir = DirPath
elif DirOk == 'n':
    UseDir = input("input full file path")


OriginList = os.listdir(UseDir)


print("working with these files:", FilteredList)
ListOk = get_cmd_input("delete these files? (y/n)","y","n")
for f in FilteredList:
    os.remove(f)

def get_cmd_input(opttext, opt1, opt2):
    while True:
        func_ans = input(opttext)
        if func_ans == opt1:
            return opt1
            break
        elif func_ans == opt2:
            return opt2
            break
        else:
            print("answer must be", opt1, "or", opt2)
