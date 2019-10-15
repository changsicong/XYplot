#coding=gbk
import sys
import os
import threading
import string
import numpy as np
import logging
#from Tkinter import *
#import tkFileDialog
from tkinter import *
import tkinter.filedialog
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.gridspec as gridspec #调整subplot的相对大小
def get_min_bound(int1,dt):
    i=0
    while i>int1:
        i=i-dt
    return i
def get_max_bound(int1,dt):
    i=0
    while i<int1:
        i=i+dt
    return i
def read_data():
    global infile,x,y,xlabel,ylabel
    fn=os.path.basename(infile)
    f=open(infile,'r')
    colx=0
    coly=1
    colz=1
    if fn=='AD1_0.txt' or fn=='AD2_0.txt':
        coly=0
        colz=1
        str=f.readline()
        str=f.readline()
        str=f.readline()
        str=f.readline()
        xlabel='step'
        ylabel='N(kN)'
    elif fn=='1_0.txt':
        colx=1
        coly=0
        str=f.readline()
        str=f.readline()
        str=f.readline()
        str=f.readline()
        str=f.readline()
        xlabel='step'
        ylabel='N(kN)'
    elif fn=='2_0.txt':
        colx=2
        coly=1
        str=f.readline()
        str=f.readline()
        str=f.readline()
        str=f.readline()
        str=f.readline()
        xlabel='D(mm)'
        ylabel='Q(kN)'
    else:
        str=f.readline()
        str=f.readline()
        items = str.split()
        if len(items)==2:
            colx=0
            coly=1
        else:
            colx=0
            coly=0
        xlabel=''
        ylabel=''
    i=0
    while str!="":
        items = str.split()
        if len(items)!=0:
            if fn=='1_0.txt' or len(items)==1:
                x0=i
            else:
                x0=float(items[colx])
            y0=float(items[coly])
            x.append(x0)
            y.append(y0)
            i+=1
        str=f.readline()
    f.close()
    print('read file ok\n')
    

def drawPic():
    global x,y,xlabel,ylabel
    x1=[]
    y1=[]
    t1=[]
    t=[]
    for i,j in enumerate(y):
        t.append(i)
    i=0
    for i in range(0,len(x)-1):
        x0=float(x[i])
        y0=float(y[i])
        t0=i
        x1.append(x0)
        y1.append(y0)
        t1.append(i)
        i+=1
        drawPic.f.clf()

        #ax1=drawPic.f.add_subplot(111,axisbg=(0.1843,0.3098,0.3098))
        #gs = gridspec.GridSpec(2, 1, width_ratios=[1,1], height_ratios=[4,1])
        gs = gridspec.GridSpec(2, 1, height_ratios=[4,1])
        #ax1=drawPic.f.add_subplot(211)

        #ax1 = plt.subplot(gs[0])
        ax1 = drawPic.f.add_subplot(gs[0])

        xmin=min(x)
        xmax=max(x)
        ymin=min(y)
        ymax=max(y)
        x_min_bound=get_min_bound(int(1.1*xmin),1)
        x_max_bound=get_max_bound(int(1.1*xmax),1)
        y_min_bound=get_min_bound(int(1.1*ymin),1)
        y_max_bound=get_max_bound(int(1.1*ymax),1)

        #threading._sleep(0.5)
        ax1.set_xlim([1.0*x_min_bound,1.0*x_max_bound])
        ax1.set_ylim([1.0*y_min_bound,1.0*y_max_bound])
        ax1.plot(x1, y1, linewidth=0.5,color='r')
        ax1.scatter(x0,y0,s=50,color='b')
        ax1.set_xlabel(xlabel)
        ax1.set_ylabel(ylabel)
        ax1.grid(True)
        if ymax>15000:
            ax1.set_yticks(range(y_min_bound,y_max_bound,1000))
        elif ymax>500:
            ax1.set_yticks(range(y_min_bound,y_max_bound,100))
        for tick in ax1.xaxis.get_major_ticks():
            tick.label1.set_fontsize(9)
        for tick in ax1.yaxis.get_major_ticks():
            tick.label1.set_fontsize(9)
        draw2(t,t1,t0,y,y1,y0,gs)
        drawPic.canvas.draw()
    print("end")
def draw2(t,t1,t0,y,y1,y0,gs):        
    #ax2=drawPic.f.add_subplot(212)
    #ax2 = plt.subplot(gs[1])
    ax2 = drawPic.f.add_subplot(gs[1])
    tmin=min(t)
    tmax=max(t)
    ymin=min(y)
    ymax=max(y)
    t_min_bound=0
    t_max_bound=len(y)
    y_min_bound=get_min_bound(int(1.1*ymin),1)
    y_max_bound=get_max_bound(int(1.1*ymax),1)
    #threading._sleep(0.5)
    ax2.set_xlim([1.0*t_min_bound,1.0*t_max_bound])
    ax2.set_ylim([1.0*y_min_bound,1.0*y_max_bound])
    ax2.plot(t, y, linewidth=0.5,color='#708090')
    ax2.plot(t1, y1, linewidth=0.5,color='r')
    ax2.scatter(t0,y0,s=50,color='b')
    for tick in ax2.xaxis.get_major_ticks():
        tick.label1.set_fontsize(9)
    for tick in ax2.yaxis.get_major_ticks():
        tick.label1.set_fontsize(9)

def openFile():    
    global infile,x,y,xlabel,ylabel
    x=[]
    y=[]
    #python2.7
    #infile=tkFileDialog.askopenfilename(filetypes=[("Load or Disp files",".txt")])
    #python3
    infile = tkinter.filedialog.askopenfilename(filetypes=[("Load or Disp files",".txt")])
    logger.info(infile)
    read_data()

if __name__ == '__main__':
    global infile,x,y,xlabel,ylabel
    #-------------------log
    #logging.basicConfig(level=logging.DEBUG)
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    x=[]
    y=[]
    #matplotlib.use('TkAgg')
    #matplotlib.rcParams['figure.facecolor']='w'
    root=Tk()

    root.withdraw()    #hide window
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight() - 100
    #under windows, taskbar may lie under the screen
    root.resizable(False,False)

    #add some widgets to the root window...
    #drawPic.f = plt.figure(figsize=(9.5,6), dpi=100) 
    drawPic.f = Figure(figsize=(9.5,6), dpi=100) 
    drawPic.f.subplots_adjust(left=0.08,right=0.95,bottom=0.05,top=0.95) 
    #drawPic.f.subplots_adjust(left=0.08,right=0.95) 
    drawPic.canvas = FigureCanvasTkAgg(drawPic.f, master=root)
    #drawPic.canvas.draw()
    drawPic.canvas.draw()
    drawPic.canvas.get_tk_widget().grid(row=0, columnspan=3)    
    Button(root,text='Open',command=openFile).grid(row=1,column=0)
    Button(root,text='Start',command=drawPic).grid(row=1,column=1,columnspan=3)

    root.update_idletasks()
    root.deiconify()    #now window size was calculated
    root.withdraw()     #hide window again
    #python3 error 
#    root.geometry('%sx%s+%s+%s' % (root.winfo_width() + 10, root.winfo_height() + 10, (screen_width - root.winfo_width())/2, (screen_height - root.winfo_height())/2) )    #center window on desktop
    root.deiconify()    

    
    #启动事件循环
    root.mainloop()
