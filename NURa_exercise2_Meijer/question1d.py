#!/usr/bin/env python3
import numpy as np
from question1 import n,Nsat,a,b,c
from question1a import A

def analytical_dndx(x,A,Nsat,a,b,c):
    '''
    Analytical derivative of the function n(x,A,Nsat,a,b,c)
    '''
    return n(x,A,Nsat,a,b,c) * ( (a-3) - c * (x/b)**c ) / x

def derivative_centraldifference(func,x,h):
    '''
    Calculate the derivative of function func, at x, 
    '''
    return (func(x+h) - func(x-h)) / (2*h)

def derivative_Ridders(func,x,target_accuracy,m=5):
    '''
    Calculate the derivative of function func, at x
    Return when the difference between the current and previous guess is smaller than target_accuracy
    '''
    h = .1 # starting step size
    d = 2  # factor to decrease h with
    
    # Initial guesses
    D = np.zeros(m)
    for i in range(m):
        D[i] = derivative_centraldifference(func,x,h)
        h /= d
    guesses = [D[0]]
    
    # Combine the initial guesses
    for k in range(1,m):
        previousguess = D[0]
        for i in (range(m-k)):
            j = i+k
            D[i] = (d**(2*j) * D[i+1] - D[i] ) / (d**(2*j) - 1)
            
        guesses.append(D[0])
        if abs(D[0]-previousguess) < target_accuracy:
            # Return if the result is accurate enough
            return D[0]
    
    # If the end result with the initial m was not accurate enough, add more m
    h /= d
    D = np.append(D,derivative_centraldifference(func,x,h))
    m += 1
    while abs(previousguess-D[0]) > target_accuracy:
        previousguess = D[0]
        for i in reversed(range(m-1)):
            j = m-1
            D[i] = (d**(2*j) * D[i+1] - D[i] ) / (d**(2*j) - 1)
            
        guesses.append(D[0])
        if abs(D[0]-previousguess) < target_accuracy:
            # Return if the result is accurate enough
            return D[0]
        
        h /= d
        D = np.append(D,derivative_centraldifference(func,x,h))
        m += 1 
        
    '''
    !!! terminate early if the error grows, and return the best approximation from before that point.
    '''

output1d = open("question1d_output.txt","w")

output1d.write("Analytical derivative at x=1 : "+str(analytical_dndx(1,A,Nsat,a,b,c)))
output1d.write("\nNumerical derivative at x=1  : "+str(derivative_Ridders(func=lambda x: n(x,A,Nsat,a,b,c),x=1,target_accuracy=1e-10)))
# !!! Target accuracy of 1e-10 is best, vanaf 1e-11 krijg je erratic errors

output1d.close()