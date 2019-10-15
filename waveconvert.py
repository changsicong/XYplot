#coding=gbk
#生成sap和abaqus时程分析的波文件
from pylab import *
import sys
import os
import string
#import tkFileDialog
import tkinter.filedialog

#infile=tkFileDialog.askopenfilename(filetypes=[("wave files","*")])
#infiles=tkFileDialog.askopenfilenames(filetypes=[("wave files","*")])
infiles=tkinter.filedialog.askopenfilenames(filetypes=[("wave files","*")])
#items=infiles.split()
for infile in infiles:
    print(infile)
    f=open(infile,'r')
    skipline = 1 #跳过的行数
    dt = 0.02 #delta T
    eqmul = 1 #放大系数
    export_time_flag = True
    normflag = 1 #归一化, 1为归一
    #每隔几个点输入一个数
    spacet = 1

    colx=0
    coly=1
    colz=4
    acc=[]
    time=[]
    x=[]
    y=[]
    z=[]
    tmpstr=f.readline()
    row=1
    while tmpstr!="":
        if row>skipline:
            items = tmpstr.split()
            acc.extend(items)
            #x.append(float(items[colx]))
            #y.append(float(items[coly]))
            #z.append(float(items[colz]))
        tmpstr=f.readline()
        row = row + 1
    f.close()
    t = 0
    for data in acc:
        time.append(t)
        y.append(float(data)*eqmul) #由字符转换为数字
        t = t + dt

    print('max:%9.7f, min:%9.7f' %(max(y),min(y)))
    ymax = max(abs(max(y)),abs(min(y)))

#------------------------------------------------
    f,ext=os.path.splitext(infile)
    fname = f + "_O.txt"
    fout = open(fname,"w")
    t = 0.0
    i=1
    i1=1
    for data in acc:
      a = float(data)*eqmul
      if normflag == 1:
          a = a/ymax
      if export_time_flag == True and i1 == i:
        fout.write('%6.4f\t%E\n' %(t,a))
        t = t + dt;
        i+=spacet
      elif export_time_flag == False and i1 == i:
        fout.write('%E\n' %a)
      i1+=1
    fout.close()

# abaqus wave
    fname = f + ".inp"
    fout = open(fname,"w")
    t = 0.0
    num = 1
    num1 = 0
    tmpstr = ''
    for data in acc:
      num = num + 1
      num1 = num1+1
      a = float(data)*eqmul
      if normflag == 1:
          a = a/ymax
      tmpstr = tmpstr + str(t) + ',' + data +','
      if num > 4:
        tmpstr = tmpstr[0:len(tmpstr)-1]
        fout.write(tmpstr)
        fout.write('\n')
        num = 1
        tmpstr = ''
      elif num1 == len(acc):
        tmpstr = tmpstr[0:len(tmpstr)-1]
        fout.write(tmpstr)
        fout.write('\n')
      t = t + dt
    fout.close()

    print("earthquake data file is exported successfully!")

    plot(time, y, linewidth=1.0)
#plot(x, z, linewidth=1.0)
    xlabel('T (s)')
    ylabel('Acc')
    title('acceleration vs. time')
    grid(True)
    show()

