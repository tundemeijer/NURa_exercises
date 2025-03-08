#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(1)
N_generate = 10000

A=1. # to be computed
Nsat=100
a=2.4
b=0.25
c=1.6

def n(x,A,Nsat,a,b,c):
    return A*Nsat*((x/b)**(a-3))*np.exp(-(x/b)**c)

output1a = open("question1a_output.txt","w")

xmin, xmax = 10**-4, 5
xdata = np.linspace(xmin,xmax,100)

# Write a numerical integrator based on some form of Richardson extrapolation to 
# solve equation (2) for A given those four parameters. Output A to full precision.
def integration_Romberg(func,a,b,m):
    '''
    Integrate the function func from a to b, at order m
    Fails if func(a) or func(b) is nan
    '''
    # Sample the function at the required points
    xdata = np.linspace(a,b,2**(m-1)+1)
    ydata = func(xdata)
    
    # Fill the first column
    r = np.zeros(m)
    N = 1
    for i in range(m):
        h = (b-a)/N
        # Use slicing to select the relevant sampled points
        r[i] = h * ( np.sum(ydata[::int((len(ydata)-1)/N)]) - 0.5*(ydata[0]+ydata[-1]) )
        N *= 2
    
    # Combine the guesses
    N = 1
    for i in range(1, m):
        N *= 4
        for j in range(0, m-i):
            r[j] = (N * r[j+1] - r[j]) / (N - 1)
 
    return r[0]

# Test whether the integration function makes sense
func = lambda x: x**2
int_func = lambda x: 1/3 * x**3
#print("Analytical:",int_func(3)-int_func(1))
#print("Romberg   :",integration_Romberg(func,1,3,m=3))


def integreer(x):
    # !!! kies welke van deze twee formuleringen mooier is
    return 4*np.pi * x**2 * ((x/b)**(a-3))*np.exp(-(x/b)**c) * A
    return 4*np.pi * x**2 * n(x) / Nsat


A = 1/integration_Romberg(integreer
                          ,xmin,xmax,m=10)
print(A)
output1a.write("A: "+str(A))


ydata = n(xdata,A,Nsat,a,b,c)
plt.loglog(xdata,ydata)
plt.xlabel("x")
plt.ylabel("n(x)")
plt.title("n(x)")
plt.show()

# Test of A consistent is, dit zou Nsat=100 moeten zijn:
print(integration_Romberg(lambda x: 4*np.pi *x**2 * n(x,A,Nsat,a,b,c),
                          xmin,xmax,m=10))

output1a.close()

#%% Question 1b

# We want to generate 3D satellite positions such that they statistically 
# follow the satellite profile in equation (1); 
# that is, the probability distribution of the (relative)
# radii x in [0, 5) should be p(x) dx = N (x) dx/ hN sat i.
# Use one of the methods discussed in class to sample this distribution.
# transformation kan niet zomaar want N(x) is niet invertible
def N(x):
    '''
    n(x) integrated over unit sphere
    '''
    return 4*np.pi * x**2 * n(x,A,Nsat,a,b,c)


def random_uniform(low=0.0, high=1.0, size=None):
    '''
    !!! vervang door zelfgeschreven functie!
    '''
    return np.random.uniform(low=low, high=high, size=size)

def rejectionsample(func,N=1,a=0,b=1):
    '''
    Draw N points from function func, between a and b
    '''
    #fig,ax = plt.subplots()
    ydata = func(xdata)
    maxy = max(ydata)
    #ax.plot(xdata,ydata)
    drawn = []
    while len(drawn)<N:
        xdraw = random_uniform() * (b-a) + a
        ydraw = random_uniform() * maxy
        #col = 'k'
        if func(xdraw)>ydraw:
            drawn.append(xdraw)
            #col = 'r'
            
        #ax.plot(xdraw,ydraw,'.',color=col)
    #plt.show()
    return np.array(drawn)

'''
# Test whether rejectionsample makes sense
func = lambda x: x/12.5

N_generate = 10000
samples = rejectionsample(func,N_generate,xmin,xmax)

edges = 10**np.linspace(np.log10(xmin), np.log10(xmax), 21)
hist = np.histogram(rejectionsample(func,N_generate,xmin,xmax), bins=edges)[0]
bin_widths = np.zeros(len(edges)-1)
for i in range(len(bin_widths)):
    bin_widths[i] = edges[i+1]-edges[i]
hist_scaled = hist/bin_widths/N_generate # divide every bin by its width

plt.hist(samples, density=True)
plt.plot(xdata,func(xdata))
#plt.stairs(hist_scaled, edges=edges, edgecolor='k', fill=True)
plt.hist(edges[:-1], edges, weights=hist_scaled,edgecolor='k')
plt.show()
'''

#%

#Plot of histogram in log-log space with line (question 1b)
xmin, xmax = 10**-4, 5
N_generate = 10000

#21 edges of 20 bins in log-space
edges = 10**np.linspace(np.log10(xmin), np.log10(xmax), 21)

galaxies = rejectionsample(N,N_generate,xmin,xmax)
hist = np.histogram(galaxies, bins=edges)[0]
bin_widths = np.zeros(len(edges)-1)
for i in range(len(bin_widths)):
    bin_widths[i] = edges[i+1]-edges[i]
hist_scaled = hist/bin_widths/N_generate # divide every bin by its width, correct for N_generate

relative_radius = np.linspace(xmin,xmax,100)#edges.copy() #replace!
analytical_function = N(relative_radius)/Nsat # correct for Nsat

fig1b, ax = plt.subplots()
ax.stairs(hist_scaled, edges=edges, edgecolor='k', fill=True, label='Satellite galaxies') #just an example line, correct this!
#ax.plot(edges[:-1], hist_scaled,'.')
plt.plot(relative_radius, analytical_function, 'r-', label='Analytical solution') #correct this according to the exercise!
ax.set(xlim=(xmin, xmax), ylim=(10**(-3), 10), 
       yscale='log', xscale='log',
       xlabel='Relative radius', ylabel='Number of galaxies')
ax.legend()
plt.savefig('plots/question1b.png', dpi=600)


#%% Question 1c
#Select 100 random satellite galaxies from (b) in a way that is guaranteed to:
# 1. select every galaxy with equal probability;
# 2. not draw the same galaxy twice;
# 3. not reject any draw.

galaxies_pool = galaxies.copy()
selection = np.array([])
for i in range(100):
    # Decide which unselected galaxy to take
    idx = int(random_uniform(low=0, high=len(galaxies_pool)))
    selection = np.append(selection, galaxies_pool[idx])
    # Remove the selected galaxy from the pool, so we can't take it again
    galaxies_pool = np.delete(galaxies_pool, idx)

print(galaxies_pool.shape, selection.shape)
plt.show()
#plt.hist(galaxies)
#plt.show()
#plt.hist(np.array(selection))
#plt.show()
# The histograms have about the same shape, which is good

#%
# Next sort the 100 drawn galaxies from smallest to largest radius

def selectionsort(arr):
    '''
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


#%
# plot the number of galaxies within a radius, use a xlog plot from x = 10 -4 to x = x max .

#Cumulative plot of the chosen galaxies (1c)
chosen = selectionsort(selection)
fig1c, ax = plt.subplots()
ax.plot(chosen, np.arange(100))
ax.set(xscale='log', xlabel='Relative radius', 
       ylabel='Cumulative number of galaxies',
       xlim=(xmin, xmax), ylim=(0, 100))
plt.savefig('plots/question1c.png', dpi=600)




plt.show()

#%% Question 1d

# Numerically calculate dn(x)/dx at x = 1.
# Output the value found alongside the analytical result, both to at least 12 significant digits. 
# Choose your differentiation algorithm such that these are as close as possible.


def analytical_dndx(x,A=A,Nsat=Nsat,a=a,b=b,c=c):
    return n(x,A,Nsat,a,b,c) * ( (a-3) - c * (x/b)**c ) / x


def derivative_centraldifference(func,x,h):
    return (func(x+h) - func(x-h)) / (2*h)

def derivative_Ridders(func,x,target_accuracy,m=5):
    h = .1
    d = 2
    D = np.zeros(m)
    for i in range(m):
        D[i] = derivative_centraldifference(func,x,h)
        h /= d
    guesses = [D[0]]
    for k in range(1,m):
        previousguess = D[0]
        for i in (range(m-k)):
            j = i+k
            D[i] = (d**(2*j) * D[i+1] - D[i] ) / (d**(2*j) - 1)
            
        guesses.append(D[0])
        if abs(D[0]-previousguess) < target_accuracy:
            # Return if the result is accurate enough
            return D[0]
    
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
    return 

h = 0.05
xtest = np.linspace(1-h,1+h,100)
plt.plot(xtest,n(xtest,A,Nsat,a,b,c))
#plt.plot(xtest,analytical_dndx(xtest,A,Nsat,a,b,c))
plt.xlabel("x")
plt.ylabel("n(x)")
plt.title("n(x)")
plt.show()
# Dat komt wel overeen


output1d = open("question1d_output.txt","w")

output1d.write("\nAnalytical derivative at x=1 : "+str(analytical_dndx(1)))
output1d.write("\nNumerical derivative at x=1 : "+str(derivative_Ridders(func=lambda x: n(x,A,Nsat,a,b,c),x=1,target_accuracy=1e-10)))
# Target accuracy of 1e-10 is best, vanaf 1e-11 krijg je erratic errors
# Initial m maakt geen verschil in resultaat

output1d.close()

