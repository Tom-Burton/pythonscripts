#!/usr/bin/env python
import os, sys
listlength = int(os.sys.argv[1])
files = list()
cwd = os.getcwd()
for dirpath, dirname, filenames in os.walk(cwd):
    for filename in filenames:
        realpath = os.path.join(dirpath, filename)
        if 'credentials' in realpath:
          files.append(realpath)
files_sorted_by_size = sorted(files, key = lambda x: os.stat(x).st_size)
for i in range(1, listlength): 
  largest_files = files_sorted_by_size[-i]
  print(largest_files, os.stat(largest_files).st_size)
