#!/usr/bin/env python
import numpy as np
from question1 import n, Nsat,a,b,c, xmin,xmax

def integration_Romberg(func,a,b,m):
    '''
    Integrate the function func from a to b, at order m
    Fails if func(a) or func(b) is nan
    '''
    # Sample the function at the required points
    xdata = np.linspace(a,b,2**(m-1)+1)
    ydata = func(xdata)
    
    # Fill the first column
    r = np.zeros(m)
    N = 1
    for i in range(m):
        h = (b-a)/N
        # Use slicing to select the relevant sampled points
        r[i] = h * ( np.sum(ydata[::int((len(ydata)-1)/N)]) - 0.5*(ydata[0]+ydata[-1]) )
        N *= 2
    
    # Combine the guesses
    N = 1
    for i in range(1, m):
        N *= 4
        for j in range(0, m-i):
            r[j] = (N * r[j+1] - r[j]) / (N - 1)
 
    return r[0]

output1a = open("question1a_output.txt","w")

A = 1/integration_Romberg(lambda x: 4*np.pi * x**2 * n(x,1.,Nsat,a,b,c) / Nsat
                          ,xmin,xmax,m=10)

output1a.write(str(A))
output1a.close()