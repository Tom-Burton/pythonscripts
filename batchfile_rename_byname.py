#!/usr/bin/python3

import os
import re
import shutil
import glob
import sys

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

def listfiles(UseDir):
    OriginList = []
    for filename in glob.iglob(UseDir + "/" + '**', recursive=False):
        OriginList.append(filename)
    r = (re.compile(SearchTerm))
    FilteredList = list(filter(r.search, OriginList))
    print("working with these files:", FilteredList)
    return FilteredList

def listResultfiles(FilteredList):
    ResultList = list()
    for x in FilteredList:
        ResultList.append(x.replace(ToReplace, ReplaceWith))
    print("end result:", ResultList)
    return ResultList


def movefiles(UseDir):
    FilteredList = listfiles(UseDir)
    ResultList = listResultfiles(FilteredList)
    for x in range(len(FilteredList)):
        shutil.move(FilteredList[x], ResultList[x])
    print("directory contents is now:", os.listdir(UseDir))


SearchTerm = input("search for filenames containing: ")
print ("looking for filenames containing: ",SearchTerm)

DirPath = os.getcwd()
print("current directory is : " + DirPath)

DirOk = get_cmd_input("is current directory ok? (y/n)","y","n")
if DirOk == "y":
    StartDir = DirPath
elif DirOk == "n":
    StartDir = input("input full file path")

ToReplace = input("section to replace:")
ReplaceWith = input("replace with:")


RecurseList = []
for filename in glob.iglob(StartDir + "/" + '**', recursive=True):
     RecurseList.append(filename)

r = (re.compile(SearchTerm))
do_recurse = get_cmd_input(str(list(filter(r.search, RecurseList))) + "apply actions to these files with similar names in subdirectories? \n (y/n) :","y","n")
confirm = get_cmd_input("Confirm rename (y/n) :", "y", "n")
if confirm == "n":
    sys.exit(0)
elif confirm == "y":
    movefiles(StartDir)
    if do_recurse == "y":
        for root, dirs, files in os.walk(StartDir, topdown = True):
           for name in dirs:
              dir = (os.path.join(root, name))
              movefiles(dir)
