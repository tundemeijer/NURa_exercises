#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt

def Poisson_distr(mu,k, threshold=np.float32(32)):
    '''
    Compute the Poisson distribution with mean mu, at position k.
    Forces datatype to be numpy.float32 throughout.
    Accounts for overflow by using logspace: 
        log(Poisson) = k*log(mu) - mu - log(k!)
    Reduces inaccuracies due to overflow when k > approximately 128.
    '''
    mu_reservoir = mu
    k_reservoir = k
    k_step = np.float32(1)  # If mu < 1, threshold/log(mu) won't work
    if mu > 1:
        k_step = np.float32(2*int(threshold/np.log(mu)))
    
    logPoisson = np.float32(0)
    for i in np.arange(1,int(k)+1,dtype=np.float32):
        if ( (logPoisson-np.log(i)) < -threshold ):
            if (k_reservoir>=k_step):
                # Add some of k*log(mu) to prevent logPoisson from becoming too large
                logPoisson += k_step*np.log(mu)
                k_reservoir -= k_step                
            else:
                # If the remaining k_reservoir is smaller than k_step,
                # just add the remaining k*log(mu)
                logPoisson += k_reservoir*np.log(mu)
                k_reservoir -= k_reservoir
        logPoisson -= np.log(i)
        
    # Add the remaining mu and k
    logPoisson += k_reservoir*np.log(mu) - mu_reservoir
    
    return np.exp(logPoisson,dtype=np.float32)

parameters = np.array([[1,0],
                       [5,10],
                       [3,21],
                       [2.6,40],
                       [100,5],
                       [101,200]
                       ], dtype=np.float32)

# Compute results and save to text file
output = open("question1_output.txt","w")
output.write("# mu     k      Poisson(mu,k)")
for mu,k in parameters:
    Poisson = Poisson_distr(np.float32(mu),np.float32(k))
    output.write(f"\n{str(mu)}    {int(k)}    {str(Poisson)}")
output.close()



# To check the accuracy of our function, compare with the value from scipy
from scipy.stats import poisson

def plot_for_comparison(mu,k):
    x = np.arange(min(poisson.ppf(0.00001, mu),k*0.6),
                  max(poisson.ppf(0.99999, mu),k*1.1),dtype=np.float32)
    
    fig, (ax1,ax2) = plt.subplots(2, 1, sharex=True)
    ax2.hlines([1e-5,-1e-5],min(x),max(x),'gray')
    scip = poisson.pmf(x, mu)
    ax1.plot(x, scip, 'b.', ms=3, label='poisson pmf')
    ax1.vlines(x, 0, scip, colors='b',lw=1, alpha=0.5)
    
    Poisson_plot = np.zeros_like(x,dtype=np.float32)
    for i in range(len(Poisson_plot)):
        Poisson_plot[i] = Poisson_distr(np.float32(mu),x[i])
    ax2.plot(x, np.frexp(Poisson_plot)[0]-np.frexp(scip)[0],'b',label="With reservoir")
    
    Poisson_plot = np.zeros_like(x,dtype=np.float32)
    for i in range(len(Poisson_plot)):
        # Mimic the result without the reservoir by setting a veyr high threshold
        Poisson_plot[i] = Poisson_distr(np.float32(mu),x[i], threshold=1e6)
    diff = np.frexp(Poisson_plot)[0]-np.frexp(scip)[0]
    ax2.plot(x, diff,'k',label="No reservoir")
    
    ax1.vlines(k,min(scip),max(scip),'gray',linestyle="--")
    ax2.vlines(k,min(min(diff),-1e-5),max(max(diff),1e-5),'gray',linestyle="--")
    
    ax1.set_title(r"$\mu$="+str(mu)+r",  $k$="+str(k))
    ax1.set_ylabel(r"Poisson($\mu,k$)")
    ax2.set_ylabel("fractional error")
    ax2.set_xlabel(r"$k$")
    ax2.legend()
    plt.savefig("./plots/question1_{}.png".format(int(mu)),dpi=600)
    #plt.close()

plot_for_comparison(101,200)