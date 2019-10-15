#!/usr/bin/env python
#coding=gb2312
#从反应谱文件中读入给定周期处的谱值，与规范反应谱比较，找出满足误差的文件
import xlrd
import os
import os.path
import re
import types

# 多周期点选波
def checkspe1(spefile, period):
    print spefile+" ok!"
    #取得不包括目录名的文件名，如：alkdsf.spe
    p,f = os.path.split(spefile)
    #取得文件名，不包括扩展名, 如alkdsf
    f,ext = os.path.splitext(f)
    infile = open(spefile,"rb")
    str = infile.readline()
    t1 = '0'
    diff1 = '0'
    alfa1 = '0'
    alfacn1 = '0'
    str3 = spefile
    while str!="":
        items = str.split()
        if len(items) > 0: #有数据
            t2 = items[0]
            alfa2 = items[1]
            alfacn2 = items[4]
            diff2 = items[5]
            for periodi in period:
                if (float(t2) >= periodi) and (float(t1) <= periodi):
                    alfa3 = (float(alfa2)-float(alfa1))/(float(t2)-float(t1))*(periodi-float(t1))+float(alfa1)
                    alfacn3 = (float(alfacn2)-float(alfacn1))/(float(t2)-float(t1))*(periodi-float(t1))+float(alfacn1)
                    diff3 = (alfa3-alfacn3)/alfacn3
                    str1 = spefile + " " + t1 + " " + alfa1 + " " + alfacn1 + " " + diff1 + "\n"
                    str2 = spefile + " " + t2 + " " + alfa2 + " " + alfacn2 + " " + diff2 + "\n"
                    #str3 = '%s %f %f %f %f\n' %(spefile,periodi,alfa3,alfacn3,diff3)
                    tmpstr = '%f %f %f' %(alfa3,alfacn3,diff3)
                    str3 = str3 + ' '+tmpstr
                    #break
            t1 = t2
            diff1 = diff2
            alfa1 = alfa2
            alfacn1 = alfacn2
        str = infile.readline()
    infile.close()
    str3=str3+'\n'
    return str3

# 双频段选波
def checkspe2(spefile, Ta, Tg, T1, delT1, delT2):
    sumalfa1 = 0
    sumalfacn1 = 0
    sumalfa2 = 0
    sumalfacn2 = 0
    num1 = 0
    num2 = 0
    print spefile+" ok!"
    #取得不包括目录名的文件名，如：alkdsf.spe
    p,f = os.path.split(spefile)
    #取得文件名，不包括扩展名, 如alkdsf
    f,ext = os.path.splitext(f)
    infile = open(spefile,"rb")
    str = infile.readline()
    str3 = spefile
    while str!="":
        items = str.split()
        if len(items) > 0: #有数据
            t = items[0]
            # 第一频段
            if (float(t) >= Ta) and (float(t) <= Tg):
                sumalfa1 = sumalfa1 + float(items[1])
                sumalfacn1 = sumalfacn1 + float(items[4])
                num1 = num1 + 1
            # 第二频段
            if (float(t) >= T1-delT1) and (float(t) <= T1+delT2):
                sumalfa2 = sumalfa2 + float(items[1])
                sumalfacn2 = sumalfacn2 + float(items[4])
                num2 = num2 + 1
        str = infile.readline()
    sumalfa1 = sumalfa1 / num1
    sumalfacn1 = sumalfacn1 / num1
    diff1 = (sumalfa1-sumalfacn1)/sumalfacn1
    sumalfa2 = sumalfa2 / num2
    sumalfacn2 = sumalfacn2 / num2
    diff2 = (sumalfa2-sumalfacn2)/sumalfacn2
    tmpstr = '%f %f %f %f %f %f' %(sumalfa1,sumalfacn1,diff1,sumalfa2,sumalfacn2,diff2)
    str3 = str3 + ' '+tmpstr
    infile.close()
    str3=str3+'\n'
    return str3


#查找给定文件夹下面所有, .* or .xls or .txt ...... 
def find_file_by_pattern(pattern='.spe', base=".", circle=True):
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

# main
period = [0.63,1.64] # 待检查的周期
Ta = 0.1
Tg = 0.45
T1 = 1.63
delT1 = 0.2
delT2 = 0.5
method = 2
# 多周期点选波
if method==1:
    fd = os.open('周期点选波结果.txt',os.O_WRONLY|os.O_CREAT)
    tablehead = '谱文件名 '
    for t in period:
        tmpstr = '%f波谱值 %f规范谱值 %f相对偏差' %(t,t,t)
        tablehead = tablehead+tmpstr+' '
    tablehead=tablehead+'\n'
    os.write(fd,tablehead)
    ff = find_file_by_pattern()
    for fn in ff:
        str=checkspe1(fn,period)
        os.write(fd,str)
    os.close(fd)
# 双频段选波
if method==2:
    fd = os.open('双频段选波结果.txt',os.O_WRONLY|os.O_CREAT)
    tablehead = '谱文件名 '
    tmpstr = '[%f-%f]波谱值 [%f-%f]规范谱值 第1频段相对偏差 [%f-%f]波谱值 [%f-%f]规范谱值 第2频段相对偏差' %(Ta,Tg,Ta,Tg,T1-delT1,T1+delT2,T1-delT1,T1+delT2)
    tablehead = tablehead+tmpstr+' '
    tablehead=tablehead+'\n'
    os.write(fd,tablehead)
    ff = find_file_by_pattern()
    for fn in ff:
        str=checkspe2(fn,Ta,Tg,T1,delT1,delT2)
        os.write(fd,str)
    os.close(fd)



