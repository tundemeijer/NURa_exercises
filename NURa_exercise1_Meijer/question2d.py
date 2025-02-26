#!/usr/bin/env python3
import numpy as np
import timeit
from interpolator import Interpolator, x,y,xx

def solve_with_LU(x,y,xx):
    # Calculate LU matrix
    inter = Interpolator(x,y)
    coeff = inter.construct_Vandermonde()
    inter.Crout(coeff)
    
    # Compute polynomial coefficients
    c = inter.solve_from_LU(y)
    
    # Compute corresponding y-values
    inter.polynomial(xx, c)
    inter.polynomial(x, c)
    return

def solve_with_Neville(x,y,xx):
    inter = Interpolator(x,y)
    yyb = np.zeros_like(xx)
    
    # Compute y-values
    for idx in range(len(yyb)):
        yyb[idx] = inter.Neville(x,y,xx[idx])
    yb = np.zeros_like(x)
    for idx in range(len(yb)):
        yb[idx] = inter.Neville(x, y, x[idx])
    return

def solve_with_iterations(x,y,xx):
    # Calculate LU matrix
    inter = Interpolator(x,y)
    coeff = inter.construct_Vandermonde()
    inter.Crout(coeff)
    
    # Compute polynomial coefficients
    c10 = inter.iterate_LU(coeff, y, N_iter=10)
    
    # Compute corresponding y-values
    inter.polynomial(xx, c10)
    inter.polynomial(x, c10)
    return

output = open("question2d_output.txt","w")

output.write("Time to solve with LU: "+
      str(timeit.timeit('solve_with_LU(x,y,xx)', globals=globals(), number=100)))

output.write("\nTime to solve with Neville: "+
      str(timeit.timeit('solve_with_Neville(x,y,xx)', globals=globals(), number=100)))

output.write("\nTime to solve with 10 LU iterations: "+
      str(timeit.timeit('solve_with_iterations(x,y,xx)', globals=globals(), number=100)))

output.close()