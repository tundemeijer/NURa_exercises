#!/usr/bin/env python
import numpy as np
import timeit

from rootfinders import *

k=1.38e-16 # erg/K
aB = 2e-13 # cm^3 / s

psi = 0.929
Z = 0.015 # solar metallicity
Tc = 1e4 # K

A = 5e-10 # erg
xi = 1e-15 # /s

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

x1,x2 = 1,1e15

rootfinder = RootFinder()
rootfinder.acc_rel = 1e-10

output2b = open("question2b_output.txt","w")

for nH in [1e-4, 1, 1e4]:
    func = lambda T: equilibrium2(T, Z, Tc, psi, nH, A, xi)
    guesses = rootfinder.bisection(func,x1,x2)
    output2b.write(f"nH={nH}"+
        f"\nBisection found a root at {guesses[-1]}, in {len(guesses)} steps"
        )
    output2b.write("\nTime to find root with bisection: "+
          str(timeit.timeit('rootfinder.bisection(func,x1,x2)', globals=globals(), number=1000)))

    guesses = rootfinder.falseposition(func,x1,x2)
    output2b.write(
        f"\nFalse position found a root at {guesses[-1]}, in {len(guesses)} steps"
        )
    output2b.write("\nTime to find root with false position: "+
          str(timeit.timeit('rootfinder.falseposition(func,x1,x2)', globals=globals(), number=1000))+"\n\n")

output2b.close()


