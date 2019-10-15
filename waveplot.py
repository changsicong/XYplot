#coding=gbk
#from pylab import *
#���������ͷȥβ�Ĳ�
import matplotlib.pyplot as plt
import sys
import os
import string
import tkinter.filedialog
import numpy as np
# plot earthquake wave curve, can select multiple wave files.
#�õ���һ�κ����һ��10%��ֵ��ʱ��
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
        waveformat=lpara[0] #1����1�У�2����time��a
        skipline = lpara[1] #����������
        dt = lpara[2] #delta T
        eqmul = lpara[3] #�Ŵ�ϵ��
        export_time_flag = lpara[4]
        normflag = lpara[5] #��һ�� ����
        labelname= lpara[6] #����
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
        str1='��һ�δﵽ��ʱ����������ֵ10%��Ӧ��ʱ�̣�S��'
        str2='���һ�δﵽ��ʱ����������ֵ10%��Ӧ��ʱ�̣�S��'
        time1st10,timelast10=gettime10(time,acc,maxacc10)
        print('0.1*Amax: %f' %(maxacc10))
        print('%s: %f' %(str1,time1st10)) 
        print('%s: %f' %(str2,timelast10)) 
        print('��Ч����ʱ��: %f' %(timelast10-time1st10))
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
    # ���ÿ̶��ı��Ĵ�С
        for tick in ax1.xaxis.get_major_ticks():
            tick.label1.set_fontsize(9)
        for tick in ax1.yaxis.get_major_ticks():
            tick.label1.set_fontsize(9)
        #legend
    #    legend=plt.legend()
    #    for t in legend.get_texts():
    #        t.set_fontsize(12)

        plt.show()
    #��showʱ�����ܱ���png
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
#��ʽ������������,delta T,�Ŵ�ϵ��,export_time_flag,normflag��һ��,labelname,title
#1����1�У�2����time��a
#lpara=[1,0,0.005,70,True,1,"$BorregoMtn40$","BorregoMtn40"] #��̨
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





