#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 15:53:21 2025

@author: tunde
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.image import imread

image=imread("M42_128.jpg")

firstrow = image[0]
#print(firstrow)
#print(len(firstrow))

# linear interpolator
# bisection to find enclosing 
npixels = 128



def bisection(data, x):
    '''
    Find the index of the datapoint with 
    value closest but not exceeding x
    Returns an index
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
        #print(middle)
        if x < data[middle]:
            end2 = middle
        elif x > data[middle]:
            end1 = middle
        #print(end1, end2)
    print(data[end1], data[end2])
    return end1
    
points = np.linspace(0,npixels, 201)
print(points)

bisection(points, 91.3)



