#coding=gbk
#plot history wave file.
#from pylab import *
from matplotlib.widgets import MultiCursor
import matplotlib.pyplot as plt
import sys
import os
import string
import matplotlib as mpl
#import tkFileDialog
import tkinter.filedialog
def getacc(t,time,acc,specn):
# 求主要周期点对应的地震影响系数
    acc1=0
    cn1=0
    for i in range(0,len(time)-1):
        if float(time[i])<t and float(time[i+1])>t:
            acc1=acc[i]+(t-float(time[i]))*(acc[i+1]-acc[i])/(float(time[i+1])-float(time[i]))
            cn1=specn[i]+(t-float(time[i]))*(specn[i+1]-specn[i])/(float(time[i+1])-float(time[i]))
            print('%9.6f(%9.6f, %9.6f, %9.6f)' %(t,acc1,cn1,acc1/cn1))
    return acc1,cn1
#    lfiles=['usa00682_o.txt','usa01273_o.txt','usa00116_o.txt','l0047x_o.txt','l0139x_o.txt','ren70_0.55_0.05_1_o.txt','ren70_0.55_0.05_4_o.txt']
##    lfiles=['usa00682_o.txt','l0032x_o.txt','usa00116_o.txt','l0047x_o.txt','l0145x_o.txt','ren70_0.55_0.05_1_o.txt','ren70_0.55_0.05_4_o.txt']
#    lfiles=['usa00170_o.txt','l0047y_o.txt','usa00115_o.txt','l0145y_o.txt','usa00677_o.txt','ren70_0.55_0.05_2_o.txt','ren70_0.55_0.05_4_o.txt']
##    lfiles=['usa00683_o.txt','l0032y_o.txt','usa00115_o.txt','l0047y_o.txt','l0145y_o.txt','ren70_0.55_0.05_2_o.txt','ren70_0.55_0.05_4_o.txt']
#    lfiles=['usa00683_o.txt','usa01274_o.txt','usa00115_o.txt','l0047y_o.txt','l0139y_o.txt','ren70_0.55_0.05_2_o.txt','ren70_0.55_0.05_4_o.txt']


#-------------------------------------main
lfiles=[]
ywaves=[]
llabels=[]
lstyle=[]
toriiso=[]

#infile=tkFileDialog.askopenfilename(filetypes=[("speplot file","*")])
infile=tkinter.filedialog.askopenfilename(filetypes=[("speplot file","*")])
f=open(infile,'r')
tmpstr=f.readline()
rootdir=tmpstr.strip('\n\r')
print(rootdir)
tmpstr=f.readline()
items=tmpstr.split()
for data in items:
    lfiles.append(data)
print(lfiles)
tmpstr=f.readline()
items=tmpstr.split()
for data in items:
    ywaves.append(data)
print(ywaves)
tmpstr=f.readline()
items=tmpstr.split()
for data in items:
    llabels.append(data)
print(llabels)
tmpstr=f.readline()
items=tmpstr.split()
for data in items:
    lstyle.append(data)
print(lstyle)
tmpstr=f.readline()
items=tmpstr.split()
for data in items:
    toriiso.append(float(data))
print(toriiso)

mpl.rcParams['font.sans-serif'] = ['SimHei']
fig=plt.figure(figsize=[5.0,3.4])
#fig=plt.figure(figsize=[7,4.5])
#ax1=fig.add_subplot(111)
ax1=fig.add_axes([0.12,0.15,0.85,0.8])  #[left, bottom, width, height]
ymax=0
sum1=[]
ave1=[]
for i in range(0,414):
    sum1.append(0)
num=len(lfiles)
for wave in lfiles:
    index=lfiles.index(wave)
    labelname=llabels[index]
    wavefile= rootdir+'\\'+wave+'.spe'
    print(wavefile)
    f=open(wavefile,'r')
    skipline = 1 #跳过的行数
    colx=0
    coly=1
    colz=4
    acc=[]
    time=[]
    y=[]
    specn=[]
    tmpstr=f.readline()
    row=1
    i=0
    while tmpstr!="":
        if row>skipline:
            items = tmpstr.split()
            t=float(items[colx]) #不转换为float的话，非常慢且图形不对
            time.append(t)
            acc.append(float(items[coly]))
            specn.append(float(items[colz]))
            sum1[i]+=float(items[coly])
            i+=1
        tmpstr=f.readline()
        row = row + 1
    f.close()
    #输出谱偏差
    for t1 in toriiso:
        accori,cnori=getacc(t1,time,acc,specn)
    ymax1=max(max(acc),min(acc))
    if ymax1>ymax:
        ymax=ymax1
    if index==0:
        specn12=[]
        specn08=[]
        for data in specn:
            specn12.append(1.2*data)
            specn08.append(0.8*data)
        ax1.plot(time, specn08, 'g', label="$0.8GB50011$", linewidth=1.0) #内置的索引号风格
        ax1.plot(time, specn12, color='g', label="$1.2GB50011$", linewidth=1.0)
        ax1.plot(time, specn, color='b', label="$GB50011$", linewidth=2.0) 
    ax1.plot(time, acc, lstyle[index], label="$%s$" %(labelname), linewidth=1.0)
    #ax1.plot(time, acc, label='ren', linewidth=1.0)
print("平均谱")
for data in sum1:
    ave1.append(data/num)
#输出谱偏差
for t1 in toriiso:
    accori,cnori=getacc(t1,time,ave1,specn)
ax1.plot(time, ave1, 'r', label=u"波平均", linewidth=2.0) #内置的索引号风格
ax1.set_xlabel(u'周期T (s)',fontsize=9)
ax1.set_ylabel(u'地震影响系数',fontsize=9)
#ax1.set_aspect(0.1)  #y/x
#plt.ylim(0,ymax1)
#title('acceleration vs. time')
#plt.figtext(0.45,0.92,'ren',color='k',fontsize=10)
ax1.grid(True)
# 设置刻度文本的大小
for tick in ax1.xaxis.get_major_ticks():
    tick.label1.set_fontsize(9)
for tick in ax1.yaxis.get_major_ticks():
    tick.label1.set_fontsize(9)
legend=plt.legend(loc='upper right',shadow=True, labelspacing=0.06)
legend.get_frame().set_width(8)
legend.get_frame().set_height(12)
#legend.get_frame().set_facecolor('#DCDCDC')
#legend.get_title().set_fontsize(fontsize = 10)
for t in legend.get_texts():
    t.set_fontsize(9)
#moving cursor
#multi=MultiCursor(fig.canvas, (ax1,ax1), color='r', lw=1)
plt.show()
#当show时，不能保存png
jpgfile='1.png'
#plt.savefig(jpgfile,dpi=100)

