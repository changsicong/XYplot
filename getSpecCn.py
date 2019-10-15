
def makespec():
#    global speccn
#    global spectime
    specalfa=[]
    spectime=[]
    Tg=0.5
    kesai=0.04
    alfamax=0.541
    g=9.8
    #gama=0.9+(0.05-float(kesai))/(0.3+6*float(kesai))
    gama=0.9
    yita1=max(0,0.02+(0.05-float(kesai))/(4+32.0*float(kesai)))
    yita2=max(0.55,1+(0.05-float(kesai))/(0.08+1.6*float(kesai)))
    Ag=float(alfamax) # units: g
    #Ag=float(alfamax)*g  # units: m
    TB=0.1
    TC=float(Tg)
    TD=5*float(Tg)
    t=0.0
    while t<6.001:
      spectime.append(t)
      t = t+0.02
    for t in spectime:
      if float(t)>=TD:
        specalfa.append(max(0,Ag*(yita2*pow(0.2,gama)-yita1*(float(t)-5*float(Tg)))))
      elif float(t)>=TC:
        specalfa.append(Ag*pow(float(Tg)/float(t),gama)*yita2)
      elif float(t)>=TB:
        specalfa.append(Ag*yita2)
      else:
        specalfa.append(Ag*(0.45+(yita2-0.45)/TB*float(t)))
    return spectime,specalfa

spectime,specalfa=makespec()
fout = open("spectrcn.out","w")
t = 0
while t<301:
    fout.write('%f\t%f\n' %(spectime[t],specalfa[t]))
    t = t + 1
fout.close()
 
