#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 15:53:21 2025

@author: tunde
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.image import imread

import matplotlib as mpl
mpl.rcParams['font.size'] = 15

image=imread("M42_128.jpg")

firstrow = image[0] [55:80] # tijdelijk! even zichtbaarder stukje knippen
npixels = len(firstrow)

def bisection(data, x, M=2):
    '''
    From the M datapoints closest to x, return the lowest index.
    
    Doesn't work if x is an array.
    '''
    end1 = 0
    end2 = len(data)-1
    
    # to put here: check if data is strictly monotonic
    
    if (x < data[end1]) or (x > data[end2]):
        # Check that the value is actually in our range
        print("Value falls outside of data")
        return
    
    while (end2-end1)>1:
        middle = int(0.5*(end1+end2))
        if x < data[middle]:
            end2 = middle
        else: # in the case that data[idx]==x, set idx as end1
            end1 = middle
    
    # Check that all M points will fall within the data
    if (end1 - (M//2-1)) < 0:
        print("With the given M, the lowest index falls outside the dataset")
        return
    if (end1 + (M//2)) > (len(data)-1):
        print("With the given M, the highest index falls outside the dataset")
        return
    
    if (M%2 > 0) and ((x-data[end1]) < (data[end2]-x)): 
        # if M is odd, the central point should be the one closest to x
        # if x is closer to end1 than end2, we're still good
        end1 -= 1
    
    return end1 - (M//2 - 1)
'''
testx = np.linspace(0,6, 7)
print(testx)
x = 3.2
plt.plot(testx, np.ones_like(testx), 'o')

# M = 3
# x=3.2 should return 2 (3 is middle)
# x=2.7 should return 2
# x=3.7 should return 3 (4 is middle)
for x in [3.3]:
    print()
    print("x =",x)
    print("returns", bisection(testx, x, M=5))
    plt.plot(x, [1], 'o', c='r')
plt.show()
'''

def interpolator_linear(xdata, ydata, x):
    '''
    Say ydata is a function f of xdata, find f at x
    '''
    idx1 = bisection(xdata, x)
    x1, x2 = xdata[idx1], xdata[idx1+1]
    y1, y2 = ydata[idx1], ydata[idx1+1]
    return (y2-y1)/(x2-x1) * (x - x1) + y1

'''
Write a linear interpolator and apply it to the first row of the image for 201 equally spaced points.
Implement bisection to find the enclosing two grid points for each x you want to interpolate at.
Plot both the measurements from the image and the interpolated results.
'''



'''
Now write a polynomial interpolator (Neville’s algorithm) and overplot these results as well.
'''

def interpolator_Neville(xdata, ydata, x, M):
    '''
    Say ydata is a function f of xdata, find f at x
    '''
    # Identify the M tabulated points around x (order is M-1)
    idx1 = bisection(xdata, x, M)
    Mpoints = xdata[idx1:idx1+M].copy()
    #print(Mpoints)
    
    # Set the initial P_i to the values at each of these points (P_i = y_i)
    P = ydata[idx1:idx1+M].copy()
    #print(P)
    
    # Check which point is closest to x, and make the initial solution equal to this tabulated value
    
    # Loop over orders k from 1 through M-1
    for k in range(1, M):
        #print()
        for i in range(0, M-k):
            j = i+k
            #print(k, i,j)
            # i = 0, j = 1
            #P_01 = ( (x-x_0)*p_11 - (x-x_1)*p_00 ) / (x_1 - x_0)
            print(i, P)
            P_ij = ( (x-Mpoints[i])*P[i+1] - \
                    (x-Mpoints[j])*P[i] ) \
                / (Mpoints[j] - Mpoints[i])
            P[i] = P_ij
        #print(P)
    # Loop over the current intervals [x_i,x_j] (with j=i+k) with i from 0 through M-1-k
    
    # Update the P_i value for the interval, overwriting previous orders
    
    # Close the loops, save the last addition closest to x as the error estimate; P_0 holds the solution
    
    return P[0]



Npoints = 47
xdata = np.arange(npixels, dtype=float)
ydata = np.array(firstrow, dtype=float)
points = np.linspace(0, npixels-1, Npoints+2)[1:-1] # cut the outer two points, don't interpolate at the edges

interpolated_linear = np.zeros_like(points)
for i in range(len(points)):
    interpolated_linear[i] = interpolator_linear(xdata, ydata, x=points[i])

M = 3
points_Neville = np.linspace(0, npixels-1, Npoints+2)[1:-1]
interpolated_Neville = np.zeros_like(points_Neville)
for i in range(len(points_Neville)):
    interpolated_Neville[i] = interpolator_Neville(xdata, ydata, x=points_Neville[i], M=M)

fig, ax = plt.subplots(figsize=(12,8))
ax.plot(firstrow, 'o', label='data')
ax.plot(points, interpolated_linear, '.', label='linear interpolation')
ax.plot(points_Neville, interpolated_Neville, '.', label='Neville')

ax.legend()
plt.show()


# huidig probleem: (wo 12 feb 17:25)
# als Npoints groter is dan 46, bij M=3, dan is er een index out of bounds 
# had bisection() dat niet moeten vangen?










