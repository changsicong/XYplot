#coding=gbk
#from pylab import *
#可以输出掐头去尾的波
import matplotlib.pyplot as plt
import sys
import os
import string
import tkinter.filedialog
import numpy as np
# plot earthquake wave curve, can select multiple wave files.
#得到第一次和最后一次10%峰值的时间
def gettime10(time,acc,maxacc10):
    time1st10=0
    timelast10=0
    ltime=[]
    for i in range(0,len(acc)):
        if abs(acc[i])>maxacc10:
            ltime.append(float(time[i]))
    time1st10=min(ltime)
    timelast10=max(ltime)
    return time1st10,timelast10

def plotwave(lpara,FigSize):
    #infile=tkFileDialog.askopenfilename(filetypes=[("wave files","*")])
    infiles=tkinter.filedialog.askopenfilenames(filetypes=[("wave files","*")])
    #files=infiles.split()
    for infile in infiles:
        print(infile)
        f=open(infile,'r')
        waveformat=lpara[0] #1——1列；2——time，a
        skipline = lpara[1] #跳过的行数
        dt = lpara[2] #delta T
        eqmul = lpara[3] #放大系数
        export_time_flag = lpara[4]
        normflag = lpara[5] #归一化 无用
        labelname= lpara[6] #波名
        TitleName=lpara[7]

        colx=0
        coly=1
        acc=[]
        time=[]
        #y=[]
        tmpstr=f.readline()
        row=1
        t = 0
        while tmpstr!="":
            if row>skipline:
                items = tmpstr.split()
                if waveformat==1:
                    time = np.append(time, t)
                    acc = np.append(acc,eqmul*float(items[colx]))
                elif waveformat==2:
                    time = np.append(time, float(items[colx]))
                    acc = np.append(acc, eqmul*float(items[coly]))
                t+=dt
            tmpstr=f.readline()
            row = row + 1
        f.close()
        print('max:%9.7f, min:%9.7f' %(max(acc),min(acc)))
        ymax=max(abs(max(acc)),abs(min(acc)))
        maxacc10=0.1*ymax
        str1='第一次达到该时程曲线最大峰值10%对应的时刻（S）'
        str2='最后一次达到该时程曲线最大峰值10%对应的时刻（S）'
        time1st10,timelast10=gettime10(time,acc,maxacc10)
        print('0.1*Amax: %f' %(maxacc10))
        print('%s: %f' %(str1,time1st10)) 
        print('%s: %f' %(str2,timelast10)) 
        print('有效持续时间: %f' %(timelast10-time1st10))
        fig=plt.figure(figsize=FigSize)
        #ax1=fig.add_subplot(111)

        ax1=fig.add_axes([0.1,0.20,0.8,0.6])  #[left, bottom, width, height]
        ax1.plot(time, acc, label=' ', linewidth=1.0)
        #ax1.plot(time, acc, label=labelname,linewidth=1.0)
        #ax1.plot(time, acc, label='ren', linewidth=1.0)
        ax1.set_xlabel('T (s)',fontsize=9)
        ax1.set_ylabel('Acc(gal)',fontsize=9)
        ax1.set_title(TitleName)
        ax1.title.set_fontsize(9)
        #ax1.set_aspect(0.1)  #y/x
        #plt.ylim(-ymax,ymax)
        #title('acceleration vs. time')
        #plt.figtext(0.45,0.92,'ren',color='k',fontsize=10)
        ax1.grid(True)
    # 设置刻度文本的大小
        for tick in ax1.xaxis.get_major_ticks():
            tick.label1.set_fontsize(9)
        for tick in ax1.yaxis.get_major_ticks():
            tick.label1.set_fontsize(9)
        #legend
    #    legend=plt.legend()
    #    for t in legend.get_texts():
    #        t.set_fontsize(12)

        plt.show()
    #当show时，不能保存png
        jpgfile='1.png'
        #plt.savefig(jpgfile,dpi=100)
    return infiles[0],ymax,acc

def prtwave(fname,ymax,normflag,start,end,acc):
    fo=open(fname,'w')
    i=0
    for a in acc[start:end]:
        aa=float(a)
        if normflag==1:
            aa=aa/ymax
        str1='%s %f\n' %(i,aa)
        fo.write(str1)
        i+=0.02
    fo.close()


#--------------------------main        
#格式，跳过的行数,delta T,放大系数,export_time_flag,normflag归一化,labelname,title
#1——1列；2——time，a
#lpara=[1,0,0.005,70,True,1,"$BorregoMtn40$","BorregoMtn40"] #丰台
wname="H475"
wname1="$"+wname+"$"
lpara=[2,0,0.02,70,True,1,wname1,wname]
#lpara=[2,0,0.02,400,True,1,wname1,wname]
figsize=[8,2.2]
#figsize=[7,2]
fname,ymax,acc=plotwave(lpara,figsize)
#start=250
#end=1500+1
start=0
end=1250+1
fname+='.txt'
normflag=lpara[5]
dt=lpara[2]
#prtwave(fname,ymax,normflag,start,end,acc)





