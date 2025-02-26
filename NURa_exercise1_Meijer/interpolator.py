#!/usr/bin/env python3
import numpy as np
import sys
import os
import matplotlib.pyplot as plt

#data=np.genfromtxt(os.path.join(sys.path[0],"Vandermonde.txt"),comments='#',dtype=np.float64)
data=np.genfromtxt("Vandermonde.txt",comments='#',dtype=np.float64)
x=data[:,0]
y=data[:,1]
xx=np.linspace(x[0],x[-1],1001) # values of x to interpolate at

class Interpolator:
    
    def __init__(self, xdata, ydata):
        self.xdata = xdata.copy()
        self.ydata = ydata.copy()
        self.N = len(xdata)

    def matmul(self,A,B):
        '''
        Multiply the 2D matrices A and B
        Accomodates for 1D vectors as well, transposes them if needed
        In: MxN matrix A, NxL matrix B
        Out: MxL matrix AB
        '''
        # Turn 1D vectors into the appropriate shape
        if len(A.shape)==1:
            A = np.array([A])
        if len(B.shape)==1:
            B = np.transpose(np.array([B]))
            
        AB = np.zeros((len(A),len(B[0])))
        for row in range(len(AB)):
            for col in range(len(AB[0])):
                AB[row,col] = np.dot(A[row],B[:,col])
                
        if len(AB[0])==1:
            # Turn vertical vector into 1D
            return np.transpose(AB)[0]
        if len(AB)==1:
            # Turn horizontal vector into 1D
            return AB[0]
        return AB
    
    def polynomial(self,x,c):
        '''
        A polynomial of the form y = c0 + c1*x + c2*x^2 + c3*x^3 + ...
        In: x-values (array), coefficients (array)
        Out: y-values (array)
        '''
        y = np.zeros_like(x)
        for i in range(len(x)):
            for j in range(len(c)):
                y[i] += c[j]*x[i]**j
        return y
    
    def construct_Vandermonde(self):
        '''
        Construct the Vandermonde matrix for self.xdata
        Out: NxN array
        '''
        self.Vandermonde = np.zeros((self.N, self.N))
        for i in range(self.N):
            for j in range(self.N):
                self.Vandermonde[i,j] = self.xdata[i]**j
        return self.Vandermonde

    def Neville(self, xdata, ydata, x):
        '''
        Returns the value at point x of the Lagrange polynomial 
        that goes through all points [xdata,ydata]
        '''
        Mpoints = xdata.copy()
        P = ydata.copy()
        
        for k in range(1, len(xdata)):
            for i in range(0, len(xdata)-k):
                j = i+k
                P[i] = ( (x-Mpoints[i])*P[i+1] - \
                        (x-Mpoints[j])*P[i] ) \
                    / (Mpoints[j] - Mpoints[i])
        return P[0]

    def Crout(self, coeff):
        '''
        LU decomposition, uses pivoting
        In: square matrix of coefficients
        Out: LU decomposition of coefficient matrix
        '''
        LU = coeff.copy()
        N = len(LU)
        self.indx = np.arange(len(coeff))
        
        for k in range(N): # k is column
            i_max = k
            for i in range(k,N): # i is row
                # find the row with the largest (absolute) pivot candidate
                if np.abs(LU[i,k]) > np.abs(LU[i_max,k]):
                    i_max = i
            if i_max != k:
                # pivot to put the biggest index at the top
                LU[[i_max,k]] = LU[[k,i_max]]
                self.indx[k] = i_max            
            
            for i in range(k+1,N):
                LU[i,k] /= LU[k,k]
                for j in range(k+1,N):
                    LU[i,j] -= LU[i,k] * LU[k,j]

        self.LU = LU
        return LU
        
    def solve_from_LU(self, ordin):
        '''
        Solve Vc=y for c, where V is an LU matrix and y is an array of y-values (ydata)
        Only works if self.LU exists
        Out: coefficients of the polynomial that passes through all points [xdata,ydata]
        '''
        N = len(ordin)
        sol = ordin.copy()
        
        # Swap rows in the solution to match the swaps in LU
        for i in range(len(self.indx)):
            sol[[i,self.indx[i]]] = sol[[self.indx[i],i]]
        
        for i in range(N):
            # forward substitution
            for j in range(i):
                sol[i] -= self.LU[i,j]*sol[j]
        
        for i in reversed(range(N)):
            # backward substitution
            for j in range(i+1,N):
                sol[i] -= self.LU[i,j]*sol[j]
            sol[i] /= self.LU[i,i]
            
        return sol
        
    def iterate_LU(self, coeff, ordin, N_iter=1):
        '''
        Solve Vc=y for c, by iterating N_iter times for an improved accuracy
        In: V is an LU matrix and y is an array of y-values (ydata)
        Out: coefficients of the polynomial that passes through all points [xdata,ydata]
        '''        
        # Solve Vc=y for c
        c_guess = self.solve_from_LU(ordin)
        
        for i in range(N_iter):
            # Solve V dc = V c_guess - y
            c_guess -= self.solve_from_LU(self.matmul(coeff, c_guess) - ordin)
            
        return c_guess