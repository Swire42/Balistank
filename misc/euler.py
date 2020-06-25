import numpy as np
import matplotlib.pyplot as plt

alpha = 35
v0 = 277.7
x0=v0*np.cos(np.radians(alpha))
y0=v0*np.sin(np.radians(alpha))
p=0.001
tmax=10000+p

Z0=(x0,y0)
b=-0.5*(1.29)*((np.pi*0.22**2)/4)*(0.45)
g=9.81
m=0.625

def F(x,y):
    F1=(b/m)*x* np.sqrt(x**2+y**2)
    F2=(b/m)*y* np.sqrt(x**2+y**2)-g
    return (F1,F2)

def euler(x0,y0, f, n, dt):
  tabY,tabX,tabT =[y0],[x0],[0]
  for k in range(n):
    xPrime, yPrime = f(tabX[-1],tabY[-1])
    tabY.append(tabY[-1]+yPrime*dt)
    tabX.append(tabX[-1]+xPrime*dt)
    tabT.append(tabT[-1]+dt)
  return tabX,tabY,tabT

X,Y,T = euler(Z0[0],Z0[1], F, 100, 0.1)
plt.plot(T,X)
plt.show()


