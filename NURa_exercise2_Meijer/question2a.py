#!/usr/bin/env python
import numpy as np
import timeit

from rootfinders import RootFinder

k=1.38e-16 # erg/K
aB = 2e-13 # cm^3 / s

psi = 0.929
Z = 0.015 # solar metallicity
Tc = 1e4 # K

def equilibrium1(T,Z,Tc,psi):
    '''
    T   temperature of the HII region
    Z   metallicity
    Tc  stellar temperature
    psi numerical value close to one
    '''
    return psi*Tc - (0.684 - 0.0416 * np.log(T/(1e4 * Z*Z)))*T

x1,x2 = 1,1e7
func = lambda T: equilibrium1(T,Z,Tc,psi)

rootfinder = RootFinder()
rootfinder.acc_abs = 0.1

output2a = open("question2a_output.txt","w")

guesses = rootfinder.bisection(func,x1,x2)
output2a.write(
    f"Bisection found a root at {guesses[-1]}, in {len(guesses)} steps"
    )
output2a.write("\nTime to find root with bisection: "+
      str(timeit.timeit('rootfinder.bisection(func,x1,x2)', globals=globals(), number=10_000)))

guesses = rootfinder.falseposition(func,x1,x2)
output2a.write(
    f"\nFalse position found a root at {guesses[-1]}, in {len(guesses)} steps"
    )
output2a.write("\nTime to find root with false position: "+
      str(timeit.timeit('rootfinder.falseposition(func,x1,x2)', globals=globals(), number=10_000)))

output2a.close()