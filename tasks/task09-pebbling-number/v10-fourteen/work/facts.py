import functools, sys
sys.setrecursionlimit(1000000)
EDGES = [(1,2),(1,3),(2,5),(2,8),(3,4),(3,6),(3,10),(4,10),(4,11),(5,8),(5,9),(6,8),(6,10),(7,9),(7,12),(8,13),(9,12),(10,11),(12,14),(13,14)]
N=14; R=1; V=range(1,N+1); adj={v:[] for v in V}
for u,v in EDGES: adj[u].append(v); adj[v].append(u)
B={v:1<<(5*(v-1)) for v in V}
def cnt(c,v): return (c>>(5*(v-1)))&31
def enc(d): return sum(x<<(5*(v-1)) for v,x in d.items())
@functools.lru_cache(maxsize=None)
def best(c,key):
    b=0
    for u in V:
        if u!=R and cnt(c,u)>=2:
            base=c-2*B[u]
            for w in adj[u]:
                b=max(b,(1 if (u,w) in key else 0)+best(base+B[w],key))
    return b
def into(t): return tuple((u,t) for u in adj[t])
for name,cfg in [("C",{7:15,11:7,14:3,13:1}),("pocket only",{11:7}),("left only",{7:15,14:3,13:1}),("left 15 on 7 only",{7:15})]:
    C=enc(cfg); best.cache_clear()
    print(name, {t: best(C,into(t)) for t in (2,3,5,6,8,9,12,13)}, "out of 7:", best(C,tuple((7,w) for w in adj[7])), "out of 11:", best(C,tuple((11,w) for w in adj[11])), "out of 14:", best(C,tuple((14,w) for w in adj[14])),
          "L->{5,8}:", best(C,((9,5),(13,8))), "8->6:", best(C,((8,6),)), "6->3:", best(C,((6,3),)))
