#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 15:53:21 2025

@author: tunde
"""
import numpy as np
import matplotlib.pyplot as plt
import timeit

Msun = 1.988409870698051e+30# const.M_sun.to(u.kg).value
c = 299792458.0 #const.c.to(u.m/u.s).value
G = 6.6743e-11 #const.G.to(u.m**3/u.kg/u.s**2).value

def Schwarzschild(M):    
    return (2*G*M*Msun)/c**2

def Schwarzschild_fast(M):
    c_inv = 1/c
    c_inv2 = c_inv * c_inv
    return (2*G*M*Msun) * c_inv2

masses = np.random.normal(1e6, 1e5, size=10000)

#%%
print("Time to compute Schwarzschild radii with division:",
      timeit.timeit('Schwarzschild(masses)', globals=globals()))

#%%
print("Time to compute Schwarzschild radii without division:",
      timeit.timeit('Schwarzschild_fast(masses)', globals=globals()))

# can use anything simpler than numpy.hist