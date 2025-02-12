#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 15:23:14 2025

@author: tunde
"""
import numpy as np
import matplotlib.pyplot as plt

def factorial(x):
    result = 1
    for i in range(1,x+1):
        result *= i
    return result

# Test factorial function
if (factorial(0)!=1) or (factorial(1)!=1) or (factorial(3)!=6):
    print("Function factorial fails!")


def sinc(x, order):
    '''
    Compute sinc(x) using a power series expansion, to a given order.
    For order >= 10, we get an error (overflow?)
    '''
    result = 0
    for n in range(order+1):
        result += ((-1)**n * x**(2*n)) / factorial(2*n+1)    
    return result

print("We are mainly dealing with truncation error")

fig, (ax1, ax2) = plt.subplots(nrows=2, figsize=(8,10))
x = np.linspace(0,10,100)
ax1.plot(x, np.sinc(x/np.pi), label="np.sinc(x)", c='k')
for order in [6,7,8,9]:
    ax1.plot(x, sinc(x,order=order), label=f"approximation of order {order}")
    ax2.plot(x, sinc(x,order=order)-np.sinc(x/np.pi), label=f"order {order}")

ax1.set_xlabel("x")
ax2.set_xlabel("x")
ax1.legend()
ax2.legend()
ax1.set_title("sinc(x)")
ax2.set_title("Error in sinc(x) (difference with np.sinc(x))")
plt.show()



