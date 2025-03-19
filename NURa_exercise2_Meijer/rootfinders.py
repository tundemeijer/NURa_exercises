#!/usr/bin/env python3
import numpy as np

class RootFinder:
    def __init__(self):
        self.acc_abs = 1e-15
        self.acc_rel = 1e-15
        self.max_iter = 100

    def falseposition(self, func,a,b):
        '''
        Find the root of function func, between x=a and x=b
        Keep track of guesses so we can plot them if we want
        '''
        guesses = []
        for _ in range(self.max_iter):
            fa = func(a)
            fb = func(b)
            c = a - (fa*(b-a)) / (fb - fa)
            guesses.append(c)
            fc = func(c)
            
            if fa*fc<0:
                # If the root is in [a,c]
                b = c
            elif fc*fb<0:
                # If the root is in [c,b]
                a = c
            elif fc==0:
                # Sometimes c lands right on the best value,
                # which the tests above don't catch
                return guesses
            
            # Is it accurate enough?
            if abs(b-a) < self.acc_abs:
                return guesses
            if abs((b-a)/c) < self.acc_rel:
                return guesses
        # If the result is not accurate enough after max_iter steps, return nan
        return [np.nan]
    
    def bisection(self, func,a,b):
        '''
        Find the root of function func, between x=a and x=b
        Keep track of guesses so we can plot them if we want
        '''
        guesses = []
        for _ in range(self.max_iter):
            c = (a+b)*0.5
            guesses.append(c)
            
            fa = func(a)
            fb = func(b)
            fc = func(c)
            if fa*fc<0:
                # If the root is in [a,c]
                b = c
            elif fc*fb<0:
                # If the root is in [c,b]
                a = c
            elif fc==0:
                # Sometimes c lands right on the best value,
                # which the tests above don't catch
                return guesses
            
            # Is it accurate enough?
            if abs(b-a) < self.acc_abs:
                return guesses
            if abs((b-a)/c) < self.acc_rel:
                return guesses
        # If the result is not accurate enough after max_iter steps, return nan
        return [np.nan]