#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from question1 import xmin, xmax
from question1b import galaxies
from randomnumbergenerator import RandomNumberGenerator

random = RandomNumberGenerator()

def selectionsort(arr):
    '''
    Return sorted version of array
    Not stable
    '''
    N = len(arr)
    for i in range(N-1):
        i_min = i
        for j in range(i+1,N):
            if arr[j]<arr[i_min]:
                i_min = j
        if i_min != i:
            arr[[i,i_min]] = arr[[i_min,i]]
    return arr

# Select 100 random satellite galaxies
galaxies_pool = galaxies.copy()
selection = np.array([])
for i in range(100):
    # Decide which unselected galaxy to take
    idx = random.random_integer(low=0, high=len(galaxies_pool))
    selection = np.append(selection, galaxies_pool[idx])
    # Remove the selected galaxy from the pool, so we can't draw it again
    galaxies_pool = np.delete(galaxies_pool, idx)

# Sort the drawn galaxies from smallest to largest radius
chosen = selectionsort(selection)

# Plot the number of galaxies within a radius
fig1c, ax = plt.subplots()
ax.plot(chosen, np.arange(100))
ax.set(xscale='log', xlabel='Relative radius', 
       ylabel='Cumulative number of galaxies',
       xlim=(xmin, xmax), ylim=(0, 100))
plt.savefig('plots/question1c.png', dpi=600)