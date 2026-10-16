import numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from scipy.optimize import brentq
Kth=4.0; x1,y1,x2,y2=6.0,2e-9,20.0,1e-7
m=brentq(lambda mm:(x2**mm-Kth**mm)/(x1**mm-Kth**mm)-y2/y1,2.0,5.0); C=y1/(x1**m-Kth**m)
rng=np.random.default_rng(11)
dK=np.array([4.15,4.3,4.5,4.8,5.2,5.6,6.5,7.3,8.4,9.3,10.5,11.8,13.5,15.5,18,21.5,24,27,33,38])
rate=C*(dK**m-Kth**m)*np.exp(rng.normal(0,0.07,dK.size))
x=np.logspace(np.log10(4.001),2,800)
fig,ax=plt.subplots(figsize=(6.4,5.2),dpi=300)
ax.loglog(x,C*(x**m-Kth**m),"-",color="0.2",lw=1.3,label="fit, da/dN = C($\\Delta K^m$ - $\\Delta K_{th}^m$)")
ax.axvline(Kth,color="k",ls=":",lw=1.0)
ax.loglog(dK,rate,"o",ms=4.5,mfc="white",mec="k",mew=0.9,label="MIM Ti-6Al-7Nb, R = 0.1, lab air")
ax.text(4.1,2.5e-5,"$\\Delta K_{th}$ = 4.0",fontsize=9,ha="left")
ax.set_xlim(3,100); ax.set_ylim(1e-10,1e-4)
ax.set_xticks([3,4,5,6,7,8,10,20,30,40,50,60,80,100]); ax.set_xticklabels(["3","4","5","6","7","8","10","20","30","40","50","60","80","100"])
ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
ax.yaxis.set_minor_locator(matplotlib.ticker.LogLocator(base=10,subs=(2.0,5.0),numticks=20))
ax.grid(True,which="major",color="0.65",lw=0.7); ax.grid(True,which="minor",color="0.8",lw=0.5)
ax.set_xlabel("$\\Delta K$  [MPa m$^{1/2}$]"); ax.set_ylabel("da/dN  [m/cycle]")
ax.legend(loc="lower right",fontsize=8,frameon=True)
fig.tight_layout(); fig.savefig("../image.png"); fig.savefig("../image.pdf"); print("figure saved; m=",m,"C=",C)
