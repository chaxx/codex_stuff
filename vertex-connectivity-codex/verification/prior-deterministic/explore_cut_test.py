import itertools
import numpy as np

def experiment(n, trials=10000, seed=5):
    rng=np.random.default_rng(seed)
    edges=list(itertools.combinations(range(n),2)); N=len(edges)
    stars=np.zeros((1<<N,n),dtype=np.int64)
    for x in range(1<<N):
        for v in range(n):
            stars[x,v]=sum(((x>>e)&1)<<i for i,e in enumerate(j for j,(a,b) in enumerate(edges) if v in (a,b)))
    cuts=[]
    for s in range(1<<(n-1)):
        cuts.append(sum((((s>>u)&1)^((s>>v)&1))<<e for e,(u,v) in enumerate(edges)))
    choices=itertools.product(range(1<<(1<<(n-1))),repeat=n) if n==3 else range(trials)
    minp=1.; arg=None
    for choice in choices:
        tables=np.array([[(code>>a)&1 for a in range(1<<(n-1))] for code in choice]) if n==3 else rng.integers(0,2,(n,1<<(n-1)))
        t=np.array([sum(tables[v,stars[x,v]]<<v for v in range(n)) for x in range(1<<N)])
        hist=np.bincount(t,minlength=1<<n)
        cut_hist=np.bincount(t[cuts],minlength=1<<n)
        p=(hist@cut_hist)/((1<<N)*len(cuts))
        if p<minp: minp=p;arg=tables.copy()
    print(n,'min',minp,'product lower',2.**(-n),'tables',arg.tolist())
experiment(3)
experiment(4,20000)
