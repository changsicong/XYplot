#coding=gbk
#plot history wave file.
#from pylab import *
from matplotlib.widgets import MultiCursor
import matplotlib.pyplot as plt
import sys
import os
import string
import matplotlib as mpl

def getacc(t,time,acc,specn):
# 求主要周期点对应的地震影响系数
    for i in range(0,len(time)-1):
        if float(time[i])<t and float(time[i+1])>t:
            acc=acc[i]+(t-float(time[i]))*(acc[i+1]-acc[i])/(float(time[i+1])-float(time[i]))
            cn=specn[i]+(t-float(time[i]))*(specn[i+1]-specn[i])/(float(time[i+1])-float(time[i]))
            print '%9.6f(%9.6f, %9.6f, %9.6f)' %(t,acc,cn,acc/cn)
    return acc,cn
#    lfiles=['usa00682_o.txt','usa01273_o.txt','usa00116_o.txt','l0047x_o.txt','l0139x_o.txt','ren70_0.55_0.05_1_o.txt','ren70_0.55_0.05_4_o.txt']
##    lfiles=['usa00682_o.txt','l0032x_o.txt','usa00116_o.txt','l0047x_o.txt','l0145x_o.txt','ren70_0.55_0.05_1_o.txt','ren70_0.55_0.05_4_o.txt']
#    lfiles=['usa00170_o.txt','l0047y_o.txt','usa00115_o.txt','l0145y_o.txt','usa00677_o.txt','ren70_0.55_0.05_2_o.txt','ren70_0.55_0.05_4_o.txt']
##    lfiles=['usa00683_o.txt','l0032y_o.txt','usa00115_o.txt','l0047y_o.txt','l0145y_o.txt','ren70_0.55_0.05_2_o.txt','ren70_0.55_0.05_4_o.txt']
#    lfiles=['usa00683_o.txt','usa01274_o.txt','usa00115_o.txt','l0047y_o.txt','l0139y_o.txt','ren70_0.55_0.05_2_o.txt','ren70_0.55_0.05_4_o.txt']
#达美
def damei():
    rootdir='d:\\proj\\达美地震波'
    lfiles=['RG-10-1_o.txt','T45D50X1_o.txt','T45D50X2_o.txt'] #x
    llabels=['RG-10-1','T45D50X1','T45D50X2']
    lstyle=['r--','g:','y-']
    t=[1.188,1.153,1.042,2.183,2.161,1.681]
    return rootdir,lfiles,llabels,lstyle,t
#新机场连廊
def xjcll():
    rootdir='e:\\wave\\wavespe70-0.55'
    lfiles=['l0070x_o.txt','l0047x_o.txt','ren70_0.55_0.05_1_o.txt'] #x
    llabels=['H0070','H0047','HREN1']
    lstyle=['r--','g:','y-']
    t=[0.98,0.92,0.405,3.0,2.607,2.342]
    return rootdir,lfiles,llabels,lstyle,t
#钻石广场
def lzsgc():
    rootdir='e:\\wave\\wavespe70-0.55'
#    lfiles=['usa00116_o.txt','l0070x_o.txt','l0366x_o.txt','l0047x_o.txt','usa00169_o.txt','ren70_0.55_0.05_1_o.txt','ren70_0.55_0.05_4_o.txt'] #x
    lfiles=['usa00115_o.txt','l0070y_o.txt','l0366y_o.txt','l0047y_o.txt','usa00170_o.txt','ren70_0.45_0.05_2.txt','ren0.16_0.4_0.02_o.txt'] #y
    llabels=['H115','H0070','H366','H0047','H169','HREN1','HREN2']
    lstyle=['r--','g:','y-','c-','r:','k-','m-.']
    tori=1.94
    tiso=4.2
    return rootdir,lfiles,llabels,lstyle,tori,tiso
#新疆天山银川公寓
def xjtsycgy():
    rootdir='e:\\wave\\wavespe70_0.4'
    lfiles=['l0366x_o.txt','usa00116_o.txt','usa00625_o.txt','usa00691_o.txt','usa00676_o.txt','ren0.4-0.16-0.05-1_O.txt','ren0.16_0.4_0.02_O.txt'] #x
    #lfiles=['l0366y_o.txt','usa00115_o.txt','usa00626_o.txt','usa00692_o.txt','usa00677_o.txt','ren0.4-0.16-0.05-2_O.txt','ren0.16_0.4_0.02_O.txt'] #y
    llabels=['H0366','H115','H625','H691','H676','HREN1','HREN2']
    lstyle=['r--','g:','y-','c-','r:','k-','m-.']
    #t=[1.693,1.626,1.507,3.973,3.947,3.713]
    t=[1.693,1.626,1.507,3.707,3.676,3.448]
    return rootdir,lfiles,llabels,lstyle,t
#武都两水中间
def wdlszj():
    rootdir='e:\\wave\\wavespe70_0.4'
    lfiles=['l0032x_o.txt','usa00116_o.txt','usa00475.ACC','usa00169_o.txt','usa00676_o.txt','ren0.4-0.16-0.05-1_O.txt','ren0.16_0.4_0.02_O.txt'] #x
    #lfiles=['l0032y_o.txt','usa00115_o.txt','usa00476.ACC','usa00170_o.txt','usa00677_o.txt','ren0.4-0.16-0.05-2_O.txt','ren0.16_0.4_0.02_O.txt'] #y
    llabels=['H0032','H115','H475','H169','H676','HREN1','HREN2']
    lstyle=['r--','g:','y-','c-','r:','k-','m-.']
    #t=[1.188,1.153,1.042,2.183,2.161,1.681]
    t=[1.066,1.060,0.958,1.835,1.835,1.768]
    return rootdir,lfiles,llabels,lstyle,t
#武都两水侧面
def wdlscm():
    rootdir='e:\\wave\\wavespe70_0.4'
    lfiles=['l0032x_o.txt','usa00116_o.txt','usa00475.ACC','usa00169_o.txt','usa00676_o.txt','ren0.4-0.16-0.05-1_O.txt','ren0.16_0.4_0.02_O.txt'] #x
    #lfiles=['l0032y_o.txt','usa00115_o.txt','usa00476.ACC','usa00170_o.txt','usa00677_o.txt','ren0.4-0.16-0.05-2_O.txt','ren0.16_0.4_0.02_O.txt'] #y
    llabels=['H0032','H115','H475','H169','H676','HREN1','HREN2']
    lstyle=['r--','g:','y-','c-','r:','k-','m-.']
    t=[0.930,0.919,0.804,2.527,2.512,2.168]
    return rootdir,lfiles,llabels,lstyle,t
#通渭女生宿舍,同两水正面
def twnsss():
    rootdir='e:\\wave\\wavespe70_0.4'
    lfiles=['l0032x_o.txt','usa00116_o.txt','l0145x_o.txt','usa00169_o.txt','usa00676_o.txt','ren0.4-0.16-0.05-1_O.txt','ren0.16_0.4_0.02_O.txt'] #x
    #lfiles=['l0032y_o.txt','usa00115_o.txt','l0145y_o.txt','usa00170_o.txt','usa00677_o.txt','ren0.4-0.16-0.05-2_O.txt','ren0.16_0.4_0.02_O.txt'] #y
    llabels=['H0032','H115','H0145','H169','H676','HREN1','HREN2']
    lstyle=['r--','g:','y-','c-','r:','k-','m-.']
    t=[0.733,0.719,0.624,2.335,2.331,1.997]
    return rootdir,lfiles,llabels,lstyle,t
#武都两水正面
def wdlszm():
    rootdir='e:\\wave\\wavespe70_0.4'
    lfiles=['l0032x_o.txt','usa00116_o.txt','l0145x_o.txt','usa00169_o.txt','usa00676_o.txt','ren0.4-0.16-0.05-1_O.txt','ren0.16_0.4_0.02_O.txt'] #x
    #lfiles=['l0032y_o.txt','usa00115_o.txt','l0145y_o.txt','usa00170_o.txt','usa00677_o.txt','ren0.4-0.16-0.05-2_O.txt','ren0.16_0.4_0.02_O.txt'] #y
    llabels=['H0032','H115','H0145','H169','H676','HREN1','HREN2']
    lstyle=['r--','g:','y-','c-','r:','k-','m-.']
    t=[0.920,0.903,0.788,2.481,2.456,2.133]
    return rootdir,lfiles,llabels,lstyle,t
#肃南红湾小学
def hwxx():
    rootdir='e:\\wave\\wavespe70_0.4'
    #lfiles=['l0032x_o.txt','usa00676_o.txt','ren0.4-0.16-0.05-2_O.txt'] #x
    #lfiles=['l0032y_o.txt','usa00170_o.txt','ren0.16_0.4_0.02_O.txt'] #y
    #llabels=['H0032','H676','HREN2']
    #lfiles=['l0032x_o.txt','usa00116_o.txt','usa00475.ACC','usa00169_o.txt','usa00676_o.txt','ren0.4-0.16-0.05-1_O.txt','ren0.16_0.4_0.02_O.txt'] #x
    lfiles=['l0032y_o.txt','usa00115_o.txt','usa00476.ACC','usa00170_o.txt','usa00677_o.txt','ren0.4-0.16-0.05-2_O.txt','ren0.16_0.4_0.02_O.txt'] #y
    llabels=['H0032','H115','H475','H169','H676','HREN1','HREN2']
    lstyle=['r--','g:','y-','c-','r:','k-','m-.']
    t=[0.745,0.690,0.643,2.43,2.419,2.264]
    return rootdir,lfiles,llabels,lstyle,t
#河北工业大学土木学院
def hbgd():
    rootdir='e:\\wave\\wavespe55-0.55'
    #lfiles=['usa00721_o.txt','l0032x_o.txt','usa00116_o.txt','l0047x_o.txt','usa00169_o.txt','ren55_0.55_0.05_1_o.txt','ren55_0.55_0.05_2_o.txt'] #x
    lfiles=['usa00722_o.txt','l0032y_o.txt','usa00115_o.txt','l0047y_o.txt','usa00170_o.txt','ren70_0.55_0.05_1_o.txt','ren70_0.55_0.05_2_o.txt'] #y
    llabels=['H721','H0032','H115','H0047','H169','HREN1','HREN2']
    lstyle=['r--','g:','y-','c-','r:','k-','m-.']
    t=[1.068,0.936,0.916,2.845,2.803,2.617]
    return rootdir,lfiles,llabels,lstyle,t
#漳县一中
def zxyz():
    rootdir='e:\\wave\\wavespe70-0.45'
    lfiles=['usa00475_o.txt','l0032x_o.txt','usa00116_o.txt','l0047x_o.txt','l0145x_o.txt','ren70_0.45_0.05.txt','ren70_0.45_0.05_2.txt'] #x
    llabels=['H475','H0032','H115','H0047','H0145','HREN1','HREN2']
    lstyle=['r--','g:','y-','c-','r:','k-','m-.']
    t=[0.864,0.785,0.674,2.292,2.269,1.810]
    return rootdir,lfiles,llabels,lstyle,t
#临泽中医院
def lzzyy():
    rootdir='e:\\wave\\wavespe70-0.45'
    lfiles=['usa00721_o.txt','l0032x_o.txt','usa00116_o.txt','l0047x_o.txt','usa00676_o.txt','ren70_0.45_0.05.txt','ren70_0.45_0.05_2.txt'] #x
#    lfiles=['usa00722_o.txt','l0032y_o.txt','usa00115_o.txt','l0047y_o.txt','usa00677_o.txt','ren70_0.45_0.05_2.txt','ren0.16_0.4_0.02_o.txt'] #y
    llabels=['H721','H0032','H115','H0047','H676','HREN1','HREN2']
    lstyle=['r--','g:','y-','c-','r:','k-','m-.']
    t=[0.802,0.714,0.647,2.638,2.620,2.504]
    return rootdir,lfiles,llabels,lstyle,t
def yjhg():
    """
    燕郊华冠
    """
    rootdir='e:\\wave\\wavespe110_0.55'
#lfiles=['usa00721.acc','l0032x_o.txt','usa00116_o.txt','l0047x_o.txt','usa00676_o.txt','ren110_0.55_0.05_1_o.txt','ren110_0.55_0.05_2_o.txt'] #x
    lfiles=['usa00722.acc','l0032y_o.txt','usa00115_o.txt','l0047y_o.txt','usa00677_o.txt','ren110_0.55_0.05_3_o.txt','ren110_0.55_0.05_1_o.txt'] #y
    llabels=['H721','H0032','H115','H0047','H676','HREN1','HREN2']
    lstyle=['r--','g:','y-','c-','r:','k-','m-.']
    t=[1.83,3.14]
    return rootdir,lfiles,llabels,lstyle,t

#甘肃天水教学楼8.5度，0.4g
def tsjxl1():
    rootdir='e:\\wave\\wavespe110_0.4'
    lfiles=['usa00475_o.txt','usa00116_o.txt','l0145x_o.txt','l0047x_o.txt','usa00676_o.txt','ren110_0.4_0.05_x.txt','ren0.4-0.16-0.05-1_o.txt'] #x
    #lfiles=['usa00475_o.txt','usa00116_o.txt','l0145x_o.txt','usa00625_o.txt','usa00676_o.txt','ren110_0.4_0.05_x.txt','ren0.4-0.16-0.05-1_o.txt'] #x
    #lfiles=['l0032y_o.txt','usa00115_o.txt','l0145y_o.txt','usa00170_o.txt','usa00677_o.txt','ren0.4-0.16-0.05-2_O.txt','ren0.16_0.4_0.02_O.txt'] #y
    llabels=['H475','H115','H0145','H0047','H676','HREN1','HREN2']
    lstyle=['r--','g:','y-','c-','r:','k-','m-.']
    t=[0.758,0.558,0.405,2.652,2.607,2.342]
    return rootdir,lfiles,llabels,lstyle,t
def tsjxl2():
    rootdir='e:\\wave\\wavespe110_0.4'
    lfiles=['usa00475_o.txt','usa00115_o.txt','l0145x_o.txt','l0047x_o.txt','usa00676_o.txt','ren110_0.4_0.05_x.txt','ren0.4-0.16-0.05-1_o.txt'] #x
    #lfiles=['usa00475_o.txt','usa00115_o.txt','l0145x_o.txt','usa00625_o.txt','usa00676_o.txt','ren110_0.4_0.05_x.txt','ren0.4-0.16-0.05-1_o.txt'] #x
    llabels=['H475','H115','H0145','H0047','H676','HREN1','HREN2']
    lstyle=['r--','g:','y-','c-','r:','k-','m-.']
    t=[0.649,0.588,0.486,2.329,2.312,2.033]
    return rootdir,lfiles,llabels,lstyle,t
#云南大理男生宿舍
def yndlnsss():
    rootdir='e:\\wave\\yunnan70_0.4\\小震spe'
    lfiles=['549ladfn.txt','taft21.txt','SX14.txt','NORTHRNWH090.txt','LWD_DEL_AMO_BLVD_90_nor.txt','ci15.txt','NGA_2990CHICHI05.CHY107_FP.txt'] #x
    #lfiles=['549ladfn.txt','taft21.txt','SX14.txt','NORTHRNWH090.txt','LWD_DEL_AMO_BLVD_90_nor.txt','ci15.txt','CAPEMENDRIO270.txt'] #x
    llabels=['549','TAF','REN2','N90','LWD','HREN1','CAP']
    lstyle=['r--','g:','y-','c-','r-','k-','m-.']
    #t=[1.051,1.020,0.911,2.655,2.651,2.194]
    t=[1.051,1.020,0.911,2.627,2.623,2.204]
    return rootdir,lfiles,llabels,lstyle,t
#丰台站小震
def fengtaizhan():
    rootdir='e:\\wave\\fengtai\Sspe'
    #lfiles=['ren70_1_o.txt','usa00640x_o.txt','usa00952x.txt'] #x
    lfiles=['ren70_2_o.txt','usa00640y_o.txt','usa00952y.txt'] #y
    llabels=['Art01','USA00640','USA00952']
    #lstyle=['r--','g:','y-','c-','r-','k-','m-.']
    lstyle=['m-','g-','k-']
    #t=[1.051,1.020,0.911,2.655,2.651,2.194]
    t=[1.051,1.020,0.911,2.627,2.623,2.204]
    return rootdir,lfiles,llabels,lstyle,t
#磁县
def cixian():
    rootdir='e:\\wave\\wavespe70-0.55'
    lfiles=['usa00169_o.txt','l0032x_o.txt','usa00116_o.txt','l0047x_o.txt','l0070x_o.txt','ren70_0.55_0.05_1_o.txt','ren70_0.55_0.05_2_o.txt'] #x
    #lfiles=['usa00170_o.txt','l0032y_o.txt','usa00115_o.txt','l0047y_o.txt','l0070y_o.txt','ren70_0.55_0.05_3_o.txt','ren70_0.55_0.05_3_o.txt'] #y
    llabels=['H169','H0032','H115','H0047','H0070','HREN1','HREN2']
    lstyle=['r--','g:','y-','c-','r:','k-','m-.']
    t=[1.734,1.508,1.346,3.604,3.424,2.871]
    return rootdir,lfiles,llabels,lstyle,t
#-------------------------------------main
rootdir,lfiles,llabels,lstyle,toriiso=cixian() #xjtsycgy()
mpl.rcParams['font.sans-serif'] = ['SimHei']
fig=plt.figure(figsize=[5.6,3.7])
#fig=plt.figure(figsize=[7,4.5])
#ax1=fig.add_subplot(111)
ax1=fig.add_axes([0.10,0.15,0.85,0.8])  #[left, bottom, width, height]
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
    print wavefile
    f=open(wavefile,'rb')
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
            t=items[colx]
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
        #ax1.plot(time, specn08, 'g', label="$0.8GB50011$", linewidth=2.0) #内置的索引号风格
        #ax1.plot(time, specn12, color='g', label="$1.2GB50011$", linewidth=2.0)
        ax1.plot(time, specn, color='b', label="$GB50011$", linewidth=2.0) 
    ax1.plot(time, acc, lstyle[index], label="$%s$" %(labelname), linewidth=1.0)
    #ax1.plot(time, acc, label='ren', linewidth=1.0)
print "平均谱"
for data in sum1:
    ave1.append(data/num)
#输出谱偏差
for t1 in toriiso:
    accori,cnori=getacc(t1,time,ave1,specn)
ax1.plot(time, ave1, 'r', label=u"波平均", linewidth=2.0) #内置的索引号风格
ax1.set_xlabel(u'周期T (s)')
ax1.set_ylabel(u'地震影响系数')
#ax1.set_aspect(0.1)  #y/x
#plt.ylim(0,ymax1)
#title('acceleration vs. time')
#plt.figtext(0.45,0.92,'ren',color='k',fontsize=10)
ax1.grid(True)
# 设置刻度文本的大小
for tick in ax1.xaxis.get_major_ticks():
    tick.label1.set_fontsize(11)
for tick in ax1.yaxis.get_major_ticks():
    tick.label1.set_fontsize(11)
legend=plt.legend(loc='upper right',shadow=True, labelspacing=0.2)
legend.get_frame().set_width(20)
legend.get_frame().set_height(30)
#legend.get_frame().set_facecolor('#DCDCDC')
#legend.get_title().set_fontsize(fontsize = 10)
for t in legend.get_texts():
    t.set_fontsize(10)
#moving cursor
#multi=MultiCursor(fig.canvas, (ax1,ax1), color='r', lw=1)
plt.show()
#当show时，不能保存png
jpgfile='1.png'
#plt.savefig(jpgfile,dpi=100)

