import numpy as np, matplotlib, math
matplotlib.use("Agg"); import matplotlib.pyplot as plt
t1,S1,t2,S2=6.0,0.02,20.0,0.0005
k=math.log((1/S2-1)/(1/S1-1))/math.log(t2/t1); lam=t1/(1/S1-1)**(1/k)
t=np.logspace(0,2,800); S=1/(1+(t/lam)**k)
fig,ax=plt.subplots(figsize=(6.4,5.0),dpi=300)
ax.loglog(t,S,"-",color="0.15",lw=1.4)
ax.set_xlim(1,100); ax.set_ylim(1e-4,1)
ax.set_xticks([1,2,3,4,5,6,8,10,15,20,30,40,50,60,80,100]); ax.set_xticklabels(["1","2","3","4","5","6","8","10","15","20","30","40","50","60","80","100"])
ax.xaxis.set_minor_locator(matplotlib.ticker.NullLocator())
ax.yaxis.set_minor_locator(matplotlib.ticker.LogLocator(base=10,subs=(2.0,5.0),numticks=12))
ax.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
ax.grid(True,which="major",color="0.6",lw=0.7); ax.grid(True,which="minor",color="0.78",lw=0.5)
ax.set_xlabel("$t$"); ax.set_ylabel("$S(t) = P(X > t)$")
fig.tight_layout(); fig.savefig("../image.png"); fig.savefig("../image.pdf"); print("figure saved; k=",k,"lam=",lam)
