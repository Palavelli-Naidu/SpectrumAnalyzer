from time import sleep
from vpython import*
import math as m
import cmath as cm
import serial
import matplotlib.pyplot as plt


c1=canvas(background=color.black,width=1800,height=600)

class Circle:
    def __init__(self,X=0,Y=0,Color=color.red,Radius=1,Rate=25):
        self.circle=curve(color=Color,radius=0.02)
        self.X=X
        self.Y=Y
        global pause
        
        for i in range(0,101):
            self.circle.append(vector(X+Radius*m.cos((2*m.pi/100)*i) ,Y+Radius*m.sin((2*m.pi/100)*i),0))
            if pause:
                while pause:
                    pass
            if Rate:
                rate(Rate)
        

    
class Grid:
    def __init__(self,Max=10,Color=vector(0,1,1)):
        global grid ;global lab
        grid=[];lab=[]
       
        for i in range(-10,11):
            j=str(i)+'j'
            grid.append(curve(vector(i,Max,0),vector(i,-Max,0),color=Color,opacity=0,radius=0.007))
            lab.append(label(pos=vector(i+0.1,-0.1,0),text=str(i),box=False,color=color.white,height=15,opacity=0.1))
            grid.append(curve(vector(Max,i,0),vector(-Max,i,0),color=Color,opacity=0,radius=0.007))
            lab.append(label(pos=vector(0.1,i-0.1,0),text=j,box=False,color=color.white,height=15,opacity=0.1))
        
    def off(self):
        for i in grid:
            i.visible=False
            
        
        for i in lab:
            i.visible=False
            



class Axis:
    def __init__(self,title="",x_value=0,y_value=0,x_length=10,y_length=10,Color=color.white):  
        self.x_value=x_value
        self.y_value=y_value
        self.x_length=x_length
        self.y_length=y_length
        label(pos=vector(x_value+1,y_value-0.2,0),text=title,color=color.red,height=20,box=False,opacity=0)
        arrow(shaftwidth=0.03,headwidth=0.06,headheight=0.04,color=Color,pos=vector(x_value,y_value,0),length=x_length,axis=vector(1,0,0))
        arrow(shaftwidth=0.03,headwidth=0.06,headheight=0.04,color=Color,pos=vector(x_value,y_value,0),length=y_length,axis=vector(0,1,0))

global pasue
pause=False

def Button_function(b):
    global pause
    if b.text=='pause':
        b.text='run'
        pause=True
            
    else:
        b.text='pause'
        pause=False


def Txt(x,y,Text,Color,Height):
    label(pos=vector(x,y,0),text=Text,color=Color,height=Height,box=False,opacity=0)


class formula:
    def __init__(self,x,y): 

        Txt(x+0.0,y+0.0,"X",color.orange,20)     # X(K)
        Txt(x+0.1,y+0.0,"(",color.orange,20)
        
        self.k_txt1=label(pos=vector(x+0.2,y+0,0),text="K",color=color.orange,height=15,box=False,opacity=0)    # -------------------->K
        Txt(x+0.3,y+0.0,")",color.orange,20)

        Txt(x+0.5,y+0.0,"=",color.green,20)       # =
        
        self.N_txt1=label(pos=vector(x+0.7,y+0.4,0),text="N",color=color.red,height=20,box=False,opacity=0)      #-----------------------> N
        Txt(x+0.7,y+0.0,"\u03A3",color.red,40);Txt(x+0.6,y-0.3,"n=0",color.red,17)
        
        self.xn_txt=label(pos=vector(x+1.0,y+0,0),text="x(n)",color=vector(0,1,1),height=20,box=False,opacity=0)   # --------------------->x(n)       
                                                        
        Txt(x+1.4,y+0.0,"e",color.red,20)   # e               
                                                        
        Txt(x+1.5,y+0.3,"-",color.red,20)
        Txt(x+1.6,y+0.3,"(",color.red,40)
        Txt(x+1.80,y+0.3,"j2\u03C0",vector(1,0,1),16)  # j2*pi
        Txt(x+2.05,y+0.3,")",color.red,40)

        Txt(x+1.8,y+0.35,"___",color.red,20)     # /

        self.N_txt2=label(pos=vector(x+1.80,y+0.1,0),text="N",color=vector(1,0,1),height=16,box=False,opacity=0)#-------------------------->N
        
        self.k_txt2=label(pos=vector(x+2.35,y+0.3,0),text="k",color=vector(0.5,0.5,1),height=20,box=False,opacity=0)      #--------------------------->k
        Txt(x+2.55,y+0.2,"*",color.orange,20)
        self.n_txt=label(pos=vector(x+2.75,y+0.3,0),text="n",color=color.green,height=20,box=False,opacity=0)    #--------------------------->n


        


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ FFT(Fast Fourier Transform) algorithm
def fft(arr):
   n=len(arr)
   if(n==1):
       return arr
  
   w=cm.exp(-(2*m.pi/n)*1j) #---------------w
   
   po=arr[1::2] ;pe=arr[::2] #odd & even powers coefficents
   ye=fft(pe);yo=fft(po)
 
   y=[0]*n
   kl=int(n/2)
   for i in range(0,kl):
       y[i]     =(ye[i] + (w**i)*yo[i])
       y[kl+i]  =(ye[i] - (w**i)*yo[i])
   
   return y
#++++++++++++++++++++++++++++++++++++++++++++++++++++

#----------------------------------------------------------------------------------------- plot class

class plot():
    def __init__(self,x_value=0,y_value=0,n=4,Val=0,df=0,dt=0):
        self.ax=Axis(x_value=x_value,y_value=y_value) # creating the axis from the Axis calss
        self.plot=curve(color=color.red,radius=0.02)
        self.n=4
        self.Val=Val
        self.dx=self.ax.x_length/len(Val)
        if(dt):
            self.df_or_dt=dt
        else:
            self.df_or_dt=df

        for i in range(0,len(self.Val)):  # adding the points to plot the graph
            if(dt):
                self.plot.append(vector(self.ax.x_value + (self.dx)*i ,self.ax.y_value +self.Val[i]*3,0))
            else:
                arrow(shaftwidth=0.03,headwidth=0.06,headheight=0.04,color=color.red,pos=vector(self.ax.x_value + (self.dx)*i,self.ax.y_value,0),length=Val[i]/10,axis=vector(0,1,0))
            
            if(((i+1)%(2**n))==0):               # code for writing units on the x axis
                x_points =round(self.df_or_dt*(i+1),2)
                x_position =(self.dx)*((i+1))
                label(pos=vector(self.ax.x_value + x_position ,self.ax.y_value-0.2,0),text=str(x_points),color=color.red,height=15,box=False,opacity=0)

#------------------------------------------------


#***************************************************************************************** Sine wave generation 

# Main code starts from here

In=input("Enter the input Mode:")

if(In=="1"):   
    x=[]              #crating the sinewave for testing
    k=[]
    tw=[]
    for i in range(0,128):
        fs=128                            # sampling frequency fs
        t=i/128                            # time interval of 0.01 to 10.24
        tw.append(t)                        
        f1=1  
        f2=3                             # input frequency f
        f3=5
        f4=7
        wave= 0.5*m.sin(2*m.pi*f1*t) +  m.sin(2*m.pi*f2*t) + 1.5*m.sin(2*m.pi*f3*t) + 2*m.sin(2*m.pi*f4*t)
        x.append(wave)
        k.append(i)
    Val=x
else:
    Arduino=serial.Serial('com4',115200)   # data reading from the Arduino or esp32
    sleep(1)
    data_arr=[]
    while (len(data_arr)<512):
        while(Arduino.inWaiting()!=0):
            data=Arduino.readline()
            data=str(data,'utf_8')
            data=data.strip('\r\n')
            data_arr.append(int(data))
    Val=data_arr    

# print(data_arr)
# print(type(data))

#******************************************************
        
I=input("Enter the mode:")             # here selecting the mode for DFT or FFT
 
c1.camera.pos=vector(4,0,6.5)
c1.camera.axis=vector(0,0,-1)


if(I=="1"):
    
        g=Grid()
        s=formula(3.4,3)
        d=formula(3.4,1.5)                      # calling lables of formula
        cy=Circle(Color=color.red,Rate=0)     #del c1.circle
        button(text='pause',bind=Button_function)  # creation of button 


        Rate=0.01
        N=len(Val)
        time_axis=Axis(title="Time Plot",x_value=-7.1,y_value=1.3,x_length=6,y_length=2)     #time_axis object creation at (x,y)=(-10,0)
            
        d.N_txt1.text=str(N)                            #  N---------> txt
        d.N_txt2.text=str(N)                            #  N----------> txt   

        for k in range(0,N):
                
            d.k_txt1.text=str(k)                         # X(k)    K--------> txt
            d.k_txt2.text=str(k)                         # k*n---------->k  txt

            arrow_obj=[]
            for n in range(0,N):                                     # time samples plot
                arrow_obj.append(arrow(shaftwidth=0.03,headwidth=0.07,headheight=0.04,color=vector(1,0,1),pos=vector(time_axis.x_value + (time_axis.x_length/N)*n ,time_axis.y_value,0),length=Val[n],axis=vector(0,1,0)))
            sleep(1)
            for n in range(0,N):                                     # taking each sample for shifting in to cycle
                x_total=(time_axis.x_value + (time_axis.x_length/N)*n)    # totallength of each time sample from origin
                x_shift=x_total/10
                y_shift=time_axis.y_value/10
                
                arrow_obj[n].length=Val[n]
                for i in range(0,11):
                    arrow_obj[n].pos=vector(x_total - x_shift*i,time_axis.y_value - y_shift*i,0)  # movement of each time sample
                    if Rate:
                      sleep(Rate)

                arrow_obj[n].axis=vector(m.cos((2*m.pi/N)*n*k),m.sin((2*m.pi/N)*n*k),0)    # direction of arrow in cycle
                arrow_obj[n].length=Val[n]              # length of each time sample                        
                
                d.xn_txt.text=str(round(Val[n],2))                         # x(n)----------> txt                                  
                d.n_txt.text=str(n)                                        # k*n------------> n  txt
                

                if Rate:
                    sleep(Rate)
            
                if pause:
                    while pause:
                        pass
            sleep(1)
            for i in arrow_obj:
                i.visible=False
 
            r=0;im=0
            for i in range(0,N):
                r=r +  Val[i]*(m.cos((2*m.pi/N)*i*k))
                im=im + Val[i]*(m.sin((2*m.pi/N)*i*k))
            result=((r)**2+(im)**2)**(1/2)/16
            resultant=arrow(shaftwidth=0.03,headwidth=0.06,headheight=0.04,color=color.orange,pos=vector(0,0,0),length=result,axis=vector(r,im,0))

            sleep(1)
            
            freq_axis=Axis(title="Frequency Plot",x_value=1.5,y_value=-3.0,x_length=6,y_length=2)                 # frequency_axis object creation
            x_shift=(freq_axis.x_value + (freq_axis.x_length/N)*k)/50          # step movement size of x_axis length  
            y_shift=freq_axis.y_value/50                                # step movement size of x_axis length

            for i in range(0,51):                                       # movement of frequency samples
                resultant.pos=vector(x_shift*i,y_shift*i,0) 
                if Rate:     
                  sleep(Rate)
            resultant.axis=vector(0,1,0)            # making each freq sample in upword direction
            resultant.length=result;                # length of each freq sample
            sleep(1)  
else:
    xfft=fft(Val)   # calculating the fft by calling the fft function

    fw=[]
    xabs=[]
    xphase=[]
    N=len(Val)
    for i in range(0,128):
        fw.append((k[i]*fs)/N)
        xabs.append(round(abs(xfft[i]),4))
        xphase.append(cm.phase(xfft[i]))
    
    plt.plot(tw,x)        # ploting the time graph
    plt.show()

    plt.plot(fw,xabs)      # ploting the frequency plot

    plt.show()
    fs=23850

    plot(x_value=1.3, y_value=0, n=4, Val=Val, df=0, dt=1/128) # ploting the time graph
    plot(x_value=-10,y_value=-5, n=4, Val=xabs, df=fs/N, dt=0) # ploting the frequency plot

    button(text='pause',bind=Button_function)  # creation of button 

