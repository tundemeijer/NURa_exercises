#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt

class RandomNumberGenerator:
    def __init__(self, seed=3):
        self.X = np.uint64(seed)

    def generate(self):
        '''
        64-bit XOR-shift, followed by MLCG
        X is the previous random number
        X may not be 0
        '''
        self.X ^= (self.X>>np.uint64(21))
        self.X ^= (self.X<<np.uint64(35))
        self.X ^= (self.X>>np.uint64(4))
        # Return MLCG of X (modulo 2**64 happens automatically, because it's a 64-bit integer)
        return (np.uint64(2685821657736338717) * self.X)
    
    def random_float(self, low=0.0, high=1.0):
        '''
        The maximum possible value of a 64-bit integer is 2**64, 
        so multiply by 2**-64 = 5.421010862427522e-20 to get a
        random float between 0 and 1
        '''
        return (5.421010862427522e-20*self.generate()) * (high-low) + low
    
    def random_integer(self, low, high=None):
        '''
        Return an integer between low and high (if high is given),
        or between 0 and low (if high is not given)
        '''
        if not high:
            low, high = 0, low
        return int(np.uint64(low) + self.generate()%(np.uint64(high)-np.uint64(low)))


def Pearson_coefficient(x,y):
    '''
    Calculate the correlation between two arrays of numbers
    '''
    return (np.mean(x*y) - np.mean(x)*np.mean(y)) / (np.sqrt(np.var(x)) * np.sqrt(np.var(y)))   

if __name__ == "__main__":

    rand = RandomNumberGenerator()
    
    low = 0
    high = 15
    func = lambda: rand.random_float(low, high)
    
    N = 10000
    X = np.array([])
    for _ in range(N):
        X = np.append(X, func())
    
    plt.hist(X, bins=range(low,high+1))
    plt.title(f"""{N} random points\nPearson coefficient: {Pearson_coefficient(X[:-1], X[1:])}""")
    plt.savefig("plots/rngtest.png", dpi=600)
    print(Pearson_coefficient(X[:-1], X[1:]))