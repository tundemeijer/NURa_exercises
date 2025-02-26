#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt

from interpolator import Interpolator, x,y,xx

inter = Interpolator(x,y)

# Calculate LU matrix
coeff = inter.construct_Vandermonde()
LU = inter.Crout(coeff)

output = open("question2_output.txt","w")
output.write("LU matrix:\n")
output.write(str(LU))
output.close()

# Compute values for question 2a
c = inter.solve_from_LU(y)
yya = inter.polynomial(xx, c)
ya = inter.polynomial(x, c)
# Compute values for question 2b
yyb = np.zeros_like(xx)
for idx in range(len(yyb)):
    yyb[idx] = inter.Neville(x,y,xx[idx])
yb = np.zeros_like(x)
for idx in range(len(yb)):
    yb[idx] = inter.Neville(x, y, x[idx])

# Compute values for question 2c
c1 = inter.iterate_LU(coeff, y, N_iter=1)
yyc1 = inter.polynomial(xx, c1)
yc1 = inter.polynomial(x, c1)

c10 = inter.iterate_LU(coeff, y, N_iter=10)
yyc10 = inter.polynomial(xx, c10)
yc10 = inter.polynomial(x, c10)

#Plot of points with absolute difference shown on a log scale (question 2a)
fig=plt.figure()
gs=fig.add_gridspec(2,hspace=0,height_ratios=[2.0,1.0])
axs=gs.subplots(sharex=True,sharey=False)
axs[0].plot(x,y,marker='o',linewidth=0)
plt.xlim(-1,101)
axs[0].set_ylim(-400,400)

axs[0].set_ylabel('$y$')
axs[1].set_ylabel('$|y-y_i|$')
axs[1].set_xlabel('$x$')
axs[1].set_yscale('log')
line,=axs[0].plot(xx,yya,color='orange')
line.set_label('Via LU decomposition')
axs[0].legend(frameon=False,loc="lower left")
axs[1].plot(x,abs(y-ya),color='orange')
plt.savefig('plots/question2a.png',dpi=600)

#For questions 2b and 2c, add this block
line,=axs[0].plot(xx,yyb,linestyle='dashed',color='green')
line.set_label('Via Neville\'s algorithm')
axs[0].legend(frameon=False,loc="lower left")
axs[1].plot(x,abs(y-yb),linestyle='dashed',color='green')
plt.savefig('plots/question2b.png',dpi=600)

#For question 2c, add this block too
line,=axs[0].plot(xx,yyc1,linestyle='dotted',color='red')
line.set_label('LU with 1 iteration')
axs[1].plot(x,abs(y-yc1),linestyle='dotted',color='red')

line,=axs[0].plot(xx,yyc10,linestyle='dashdot',color='purple')
line.set_label('LU with 10 iterations')
axs[1].plot(x,abs(y-yc10),linestyle='dashdot',color='purple')

axs[0].legend(frameon=False,loc="lower left")
plt.savefig('plots/question2c.png',dpi=600)