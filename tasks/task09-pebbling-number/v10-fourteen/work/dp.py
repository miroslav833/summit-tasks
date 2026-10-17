import json, collections, functools, sys
sys.setrecursionlimit(1000000)
EDGES = [(1,2),(1,3),(2,5),(2,8),(3,4),(3,6),(3,10),(4,10),(4,11),(5,8),(5,9),(6,8),(6,10),(7,9),(7,12),(8,13),(9,12),(10,11),(12,14),(13,14)]
N=14; R=1; V=list(range(1,N+1)); adj={v:[] for v in V}
for u,v in EDGES: adj[u].append(v); adj[v].append(u)
B={v:1<<(5*(v-1)) for v in V}
def cnt(c,v): return (c>>(5*(v-1)))&31
def enc(cfg): return sum(x<<(5*(v-1)) for v,x in cfg.items())
OTH=[v for v in V if v!=R]
@functools.lru_cache(maxsize=None)
def best(c,key):
    b=0
    for u in OTH:
        if cnt(c,u)>=2:
            base=c-2*B[u]
            for w in adj[u]:
                b=max(b,(1 if (u,w) in key else 0)+best(base+B[w],key))
    return b
for name,cfg in [("C",{7:15,11:7,14:3,13:1}),("T2",{7:15,11:7,12:1,13:1,14:1}),("sym",{7:7,11:7,12:7,14:5})]:
    C=enc(cfg); print(name,cfg)
    print("  into {5,8} from left:",best(C,((9,5),(13,8))),"  out of 11:",best(C,((11,4),(11,10))))
    for t in (2,3,5,8,4,6,10,9,13):
        print(f"  arrivals at {t}:",best(C,tuple((u,t) for u in adj[t] if u!=R)),end=";")
    print()
