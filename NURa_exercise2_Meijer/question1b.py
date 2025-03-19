#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from question1 import n,Nsat,a,b,c, xmin, xmax
from question1a import A
from randomnumbergenerator import RandomNumberGenerator

random = RandomNumberGenerator()

def N(x):
    '''
    n(x) integrated over unit sphere
    '''
    return 4*np.pi * x**2 * n(x,A,Nsat,a,b,c)

def rejectionsample(func,N=1,xmin=0,xmax=1):
    '''
    Draw N points from function func(x), between x=xmin and x=xmax
    '''    
    # Find the height of func
    xdata = np.linspace(xmin,xmax,100)
    ydata = func(xdata)
    maxy = max(ydata)*1.1 # Safety margin of 10%
    
    drawn = []
    while len(drawn)<N:
        xdraw = random.random_float(xmin,xmax)
        ydraw = random.random_float() * maxy
        if func(xdraw)>ydraw:
            drawn.append(xdraw)
    return np.array(drawn)

#Plot of histogram in log-log space with line (question 1b)
N_generate = 10000

#21 edges of 20 bins in log-space
edges = 10**np.linspace(np.log10(xmin), np.log10(xmax), 21)

galaxies = rejectionsample(N,N_generate,xmin,xmax)
hist = np.histogram(galaxies, bins=edges)[0]
bin_widths = np.zeros(len(edges)-1)
for i in range(len(bin_widths)):
    bin_widths[i] = edges[i+1]-edges[i]
hist_scaled = hist/bin_widths/N_generate # divide every bin by its width, correct for N_generate

relative_radius = np.linspace(xmin,xmax,100)
analytical_function = N(relative_radius)/Nsat # correct for Nsat

fig1b, ax = plt.subplots()
ax.stairs(hist_scaled, edges=edges, edgecolor='k', fill=True, label='Sampled satellite galaxies')
plt.plot(relative_radius, analytical_function, 'r-', label='Analytical solution')
ax.set(xlim=(xmin, xmax), ylim=(10**(-3), 10), 
       yscale='log', xscale='log',
       xlabel='Relative radius', ylabel='Number of galaxies')
ax.legend()
plt.savefig('plots/question1b.png', dpi=600)