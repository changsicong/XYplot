#coding=gbk
from pylab import *
import sys
import os
import string
import tkFileDialog

infile=tkFileDialog.askopenfilename(filetypes=[("spe files","spe")])
f=open(infile,'rb')
x=[]
y=[]
z=[]
colx=0
coly=1
colz=4
str=f.readline()
str=f.readline()
while str!="":
    items = str.split()
    x.append(float(items[colx]))
    y.append(float(items[coly]))
    z.append(float(items[colz]))
    str=f.readline()
plot(x, y, linewidth=1.0)
plot(x, z, linewidth=1.0)
xlabel('T (s)')
ylabel('Alfamax (g)')
title('spectrum vs. time')
grid(True)
show()

