#!/usr/bin/env python
#coding=gb2312
#将cabr波库的波,由多列分割为1列1个文件
import xlrd
import os
import os.path
import re
import types
# *.acc的头部信息为2行，第二个数据是dt, 总共有0.01，0.02，0.005, 0.021，0.023五种情况
dt = 0.023 # 待检出的时间间隔
def checkwave(wavefile, checkfile):
    print wavefile+" ok!"
    #取得不包括目录名的文件名，如：alkdsf.spe
    p,f = os.path.split(wavefile)
    #取得文件名，不包括扩展名, 如alkdsf
    f,ext = os.path.splitext(f)
    infile = open(wavefile,"rb")
    str = infile.readline()
    items = str.split()
    if len(items) > 0: #有数据
        if float(items[1]) == dt:
            str1 = wavefile + "\n"
            os.write(checkfile,str1)
    infile.close()

#查找给定文件夹下面所有, .* or .xls or .txt ...... 
#注意扩展名区分大小写,将下面一行的pattern分别设为.acc和.ACC进行处理
def find_file_by_pattern(pattern='.ACC', base=".", circle=True):
    re_file = re.compile(pattern)
    if base == ".":
        base = os.getcwd()
        
    final_file_list = []
    #print base
    cur_list = os.listdir(base)
    for item in cur_list:
        if item == ".svn":
            continue
        
        full_path = os.path.join(base, item)
        if full_path.endswith(".doc") or \
            full_path.endswith(".bmp") or \
            full_path.endswith(".wpt") or \
            full_path.endswith(".dot") or \
            full_path.endswith(".inp") or \
            full_path.endswith(".py") or \
            full_path.endswith(".txt") or \
            full_path.endswith(".swp"):
            continue
            
        # print full_path
        bfile = os.path.isfile(item)
        if os.path.isfile(full_path):
           if re_file.search(full_path):
               final_file_list.append(full_path)
        else:
           final_file_list += find_file_by_pattern(pattern, full_path)
    return final_file_list

fd = os.open('wavelist.txt',os.O_WRONLY|os.O_CREAT)
ff = find_file_by_pattern()
for fn in ff:
    checkwave(fn,fd)
os.close(fd)



