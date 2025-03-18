#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt

from rootfinders import *

k=1.38e-16 # erg/K
aB = 2e-13 # cm^3 / s


# For this exercise you can choose the root finders that you prefer – however,
# whether you get full points depends on how fast the root is found (so be sure to print the number of
# steps and time taken).

# here no need for nH nor ne as they cancel out
def equilibrium1(T,Z,Tc,psi):
    '''
    T   temperature of the HII region
    Z   metallicity
    Tc  stellar temperature
    psi numerical value close to one
    '''
    return psi*Tc - (0.684 - 0.0416 * np.log(T/(1e4 * Z*Z)))*T

psi = 0.929
Z = 0.015 # solar metallicity
Tc = 1e4 # K


def compare_rootfinders(func, interval):
    fig, (ax1,ax2) = plt.subplots(1,2, figsize=(10,3))
        
    x = np.linspace(interval[0],interval[1],100)
    ax1.hlines(0, interval[0], interval[1],'gray')
    ax1.plot(x,func(x),'k')
    
    guesses = find_root_bisection(func,interval[0],interval[1])
    ax1.plot(guesses,func(np.array(guesses)),'.',label='bisection')
    ax2.plot(guesses)
    print("bisecion:",guesses[-1], f"({len(guesses)} steps)", func(guesses[-1]))
    print()
    
    guesses = find_root_secant(func,interval[0],interval[1])
    ax1.plot(guesses,func(np.array(guesses)),'.',label='secant')
    ax2.plot(guesses[10:])
    #print(guesses)
    print("secant:",guesses[-1], f"({len(guesses)} steps)", func(guesses[-1]))
    print()
    
    #guesses = find_root_newtonraphson(func,d_func,np.mean(interval))
    #ax1.plot(guesses,func(np.array(guesses)),'.',label='newtonraphson')
    #ax2.plot(guesses)
    #print("newtonraphson:",guesses[-1], f"({len(guesses)} steps)", func(guesses[-1]))
    
    guesses = find_root_falseposition(func,interval[0],interval[1])
    ax1.plot(guesses,func(np.array(guesses)),'.',label='falseposition')
    ax2.plot(guesses)
    print("falseposition:",guesses[-1], f"({len(guesses)} steps)", func(guesses[-1]))
    print()
        
    ax1.legend()
    plt.show()

interval = [1,1e7]
#interval = [32000, 33000]
eh = 32539.126737497554
margin = 0.000000000002
#interval = [eh-margin, eh+margin]
func = lambda T: equilibrium1(T,Z,Tc,psi)
d_func = lambda T: 0.0416 * np.log(T/(1e4 * Z*Z)) + 0.0416 - 0.684
#d_func = 

temps = np.linspace(interval[0], interval[1],10)
plt.plot(temps, func(temps))
plt.title("func")
#for temp in temps:
#    print(temp, func(temp))
plt.show()
#plt.plot(temps, d_func(temps))
#plt.title("d_func")
#plt.show()

compare_rootfinders(func, interval)




#%%


def equilibrium2(T,Z,Tc,psi, nH, A, xi):
    '''
    T   
    Z   metallicity
    Tc  stellar temperature
    psi numerical value close to one
    nH  hydrogen number density
    A   
    xi  
    '''
    return (psi*Tc - (0.684 - 0.0416 * np.log(T/(1e4 * Z*Z)))*T - .54 * ( T/1e4 )**.37 * T)*k*nH*aB + A*xi + 8.9e-26 * (T/1e4)

A = 5e-10 # erg
xi = 1e-15 # /s

nH = 1e-4
for nH in [1e-4,1,1e4]: # /cm3
    func = lambda T: equilibrium2(T,Z,Tc,psi, nH, A, xi)
    interval = [1,1e15]
    m = 3e14
    #interval = [160647887538652.9-m, 160647887538652.9+2*m]
    #interval = [1, 1e5]
    #interval = [1,2e4]
    compare_rootfinders(func, interval)

'''
zero = 32539.126737497554
margin = 1e-9
interval = [zero-margin, zero+margin]
temps = np.linspace(interval[0], interval[1],10)
plt.plot(temps, func(temps))
plt.title("func")
for temp in temps:
    print(temp, func(temp))
plt.show()
'''




