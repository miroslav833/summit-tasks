import numpy as np, math
def M_grid(T,k,lam,n=4000):
    h=T/n; t=np.linspace(0,T,n+1)
    F=1-1/(1+(t/lam)**k)
    f=(k/lam)*(t/lam)**(k-1)/(1+(t/lam)**k)**2
    M=np.zeros(n+1)
    for i in range(1,n+1):
        Mrev=M[i::-1]; w=np.full(i+1,h); w[0]=w[-1]=h/2
        M[i]=F[i]+np.dot(w[1:]*f[1:i+1],Mrev[1:])
    return M[-1]
def moments(k,lam):
    m=lam*(math.pi/k)/math.sin(math.pi/k)
    E2=lam**2*(2*math.pi/k)/math.sin(2*math.pi/k)
    return m,E2
def asym(T,k,lam):
    m,E2=moments(k,lam); return T/m+(E2-2*m*m)/(2*m*m)
def fit(t1,S1,t2,S2):
    k=math.log((1/S2-1)/(1/S1-1))/math.log(t2/t1); return k,t1/(1/S1-1)**(1/k)
def sf2(v): return float(f"{v:.2g}")
