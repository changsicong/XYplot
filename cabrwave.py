#!/usr/bin/env python
#coding=gb2312
#��cabr����Ĳ�,�ɶ��зָ�Ϊ1��1���ļ�
import xlrd
import os
import os.path
import re
import types
# *.acc��ͷ����ϢΪ2�У��ڶ���������dt, �ܹ���0.01��0.02��0.005, 0.021��0.023�������
dt = 0.023 # �������ʱ����
def checkwave(wavefile, checkfile):
    print wavefile+" ok!"
    #ȡ�ò�����Ŀ¼�����ļ������磺alkdsf.spe
    p,f = os.path.split(wavefile)
    #ȡ���ļ�������������չ��, ��alkdsf
    f,ext = os.path.splitext(f)
    infile = open(wavefile,"rb")
    str = infile.readline()
    items = str.split()
    if len(items) > 0: #������
        if float(items[1]) == dt:
            str1 = wavefile + "\n"
            os.write(checkfile,str1)
    infile.close()

#���Ҹ����ļ�����������, .* or .xls or .txt ...... 
#ע����չ�����ִ�Сд,������һ�е�pattern�ֱ���Ϊ.acc��.ACC���д���
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



