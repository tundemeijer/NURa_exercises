#!/usr/bin/env python
import numpy as np

def n(x,A,Nsat,a,b,c):
    return A*Nsat*((x/b)**(a-3))*np.exp(-(x/b)**c)

xmin, xmax = 10**-4, 5

Nsat=100
a=2.4
b=0.25
c=1.6
