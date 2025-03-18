#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

absolute_target_accuracy = 1e-1
relative_target_accuracy = 1e-10
max_iterations = 500

def find_root_bisection(func,a,b):
    guesses = []
    for _ in range(max_iterations):
        #print(func(a),func(b))
        c = (a+b)*0.5
        guesses.append(c)
        if func(a)*func(c)<0:
            # als de root in [a,c] zit
            #print(f"root zit tussen {a} en {c}")
            b = c
        elif func(c)*func(b)<0:
            # als de root in [c,b] zit
            #print(f"root zit tussen {c} en {b}")
            a = c
        elif func(c)==0:
            print("bisection: tegengekomen")
            return guesses
        
        # Is het accuraat genoeg?
        if (b-a)<absolute_target_accuracy:
            print("bisection: goed genoeg (absolute)")
            return guesses
        if ((b-a)/c) < relative_target_accuracy:
            print("bisection: goed genoeg (relative)")
            return guesses
    print("bisection: dat was lang genoeg")
    return guesses
    
def find_root_secant(func,a,b):
    '''
    At risk of diverging
    '''
    guesses = []
    for _ in range(max_iterations):
        c = b - (b-a)/(func(b)-func(a)) * func(b)
        guesses.append(c)
        
        if func(a)*func(c)<0:
            # als de root in [a,c] zit
            #print(f"[{a},{b}]   root zit tussen {a} en {c}")
            b = c
        elif func(c)*func(b)<0:
            # als de root in [c,b] zit
            #print(f"[{a},{b}]   root zit tussen {c} en {b}")
            a = c
        elif func(c)==0:
            print("secant: tegengekomen")
            return guesses
        
        # Is het accuraat genoeg?
        if (b-a)<absolute_target_accuracy:
            print("secant: goed genoeg (absolute)")
            return guesses
        if ((b-a)/c) < relative_target_accuracy:
            print("secant: goed genoeg (relative)")
            return guesses
    print("secant: dat was lang genoeg")
    return guesses

def find_root_newtonraphson(func,d_func,a):
    guesses = []
    for _ in range(max_iterations):
        a = a - func(a)/d_func(a)
        guesses.append(a)
    
        # Is het accuraat genoeg?
        #if (b-a)<absolute_target_accuracy:
            #print("goed genoeg (absolute)")
        #    return guesses
        #if ((b-a)/c) < relative_target_accuracy:
            #print("goed genoeg (relative)")
        #    return guesses
    #print("dat was lang genoeg")
    return guesses

def find_root_falseposition(func,a,b):
    guesses = []
    for _ in range(max_iterations):
        c = a - (func(a)*(b-a)) / (func(b) - func(a))
        guesses.append(c)
        
        if func(a)*func(c)<0:
            # als de root in [a,c] zit
            #print(f"root zit tussen {a} en {c}")
            b = c
        elif func(c)*func(b)<0:
            # als de root in [c,b] zit
            #print(f"root zit tussen {c} en {b}")
            a = c
        elif func(c)==0:
            print("falseposition: tegengekomen")
            return guesses
        
        # Is het accuraat genoeg?
        if (b-a)<absolute_target_accuracy:
            print("falseposition: goed genoeg (absolute)")
            return guesses
        if ((b-a)/c) < relative_target_accuracy:
            print("falseposition: goed genoeg (relative)")
            return guesses
    print("falseposition: dat was lang genoeg")
    return guesses