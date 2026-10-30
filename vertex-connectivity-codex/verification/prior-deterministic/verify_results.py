"""Finite sanity checks for the deterministic-connectivity research note.
These tests complement, and do not replace, the proofs. Standard library only.
Run: python verify_results.py
"""
from itertools import combinations
from math import comb
import json, random
from pathlib import Path

def is_connected(n, edges):
    adj=[0]*n
    for u,v in edges:adj[u]|=1<<v;adj[v]|=1<<u
    reached=1; frontier=1
    while frontier:
        bit=frontier&-frontier;frontier-=bit;u=bit.bit_length()-1
        new=adj[u]&~reached;reached|=new;frontier|=new
    return reached==(1<<n)-1

def edges_of(n,mask):
    return [e for j,e in enumerate(combinations(range(n),2)) if mask>>j&1]

def turan(n,p):
    q,r=divmod(n,p)
    return (n*n-r*(q+1)**2-(p-r)*q*q)//2

result={}
# Integer Mobius coefficients of connectivity, then reduce modulo small primes.
degrees={}; degree_cases=0
for n in range(2,7):
    E=list(combinations(range(n),2)); N=len(E)
    coef=[int(is_connected(n,[e for j,e in enumerate(E) if mask>>j&1])) for mask in range(1<<N)]
    for j in range(N):
        for mask in range(1<<N):
            if mask>>j&1:coef[mask]-=coef[mask^(1<<j)]
    ds={}
    for p in (2,3,5,7):
        d=max(mask.bit_count() for mask,c in enumerate(coef) if c%p)
        assert d==turan(n,p),(n,p,d,turan(n,p));ds[str(p)]=d
    degrees[str(n)]=ds;degree_cases+=len(coef)
result['algebraic_degree']={'graphs_checked':degree_cases,'degrees_by_n_and_prime':degrees}
# Every nonzero Boolean kernel direction admits the tree-overlay witness.
count=0
for n in range(2,7):
    E=list(combinations(range(n),2))
    for mask in range(1,1<<len(E)):
        D=set(e for j,e in enumerate(E) if mask>>j&1); u,v=next(iter(D))
        T={tuple(sorted((u,w))) for w in range(n) if w!=u}
        G0=T-D; G1=G0|D
        assert not is_connected(n,G0) and is_connected(n,G1)
        assert G0.symmetric_difference(G1)==D;count+=1
result['tree_overlay']={'nonzero_differences_checked':count}
# Complete-graph two-sheeted lift dichotomy.
count=0
for m in range(2,7):
    E=list(combinations(range(m),2))
    for mask in range(1<<len(E)):
        X=[[0]*m for _ in range(m)];lift=[]
        for j,(u,v) in enumerate(E):
            x=(mask>>j)&1; X[u][v]=X[v][u]=x
            for b in (0,1):lift.append((2*u+b,2*v+(b^x)))
        s=X[0];cut=all(X[u][v]==(s[u]^s[v]) for u,v in E)
        assert is_connected(2*m,lift)==(not cut);count+=1
result['two_lift']={'base_graphs_checked':count}
# All affine-plane witnesses at small m.
count=0
for m in range(3,7):
    for a in range(1,1<<(m-1)):
        av=[0]+[(a>>(i-1))&1 for i in range(1,m)]
        for b in range(1,1<<(m-1)):
            if a==b:continue
            bv=[0]+[(b>>(i-1))&1 for i in range(1,m)]
            D=[[av[u]*bv[v]^bv[u]*av[v] for v in range(m)] for u in range(m)]
            assert any(D[u][v] for u,v in combinations(range(m),2))
            assert not any(D[0])
            for s in range(1<<(m-1)):
                sv=[0]+[(s>>(i-1))&1 for i in range(1,m)]
                for v in range(m):
                    candidate=tuple(sv[i]^D[v][i] for i in range(m))
                    expected=tuple(sv[i]^(av[v]*bv[i])^(bv[v]*av[i]) for i in range(m))
                    assert candidate==expected
                count+=1
result['affine_plane']={'instances_checked':count}
# Actual equal-cardinality collisions for common additive sketches over Z/pZ.
rng=random.Random(431);count=0
for p in (2,3,5,7):
    for trial in range(200):
        n=17;m=8; U=list(range(m));W=list(range(m,2*m));h=2*m
        weights=[rng.randrange(p) for _ in range(n)]
        def witness(block):
            seen={}
            for sub in combinations(block,m//2):
                val=sum(weights[u] for u in sub)%p
                if val in seen:
                    s,t=set(sub),seen[val]
                    return s-t,t-s
                seen[val]=set(sub)
            raise AssertionError('pigeonhole witness missing')
        Ap,Am=witness(U);Bp,Bm=witness(W)
        a=min(Ap);b=min(Bp)
        common={tuple(sorted((h,a))),tuple(sorted((h,b)))}
        active=Ap|Am|Bp|Bm|{h}
        for v in set(range(n))-active:common.add(tuple(sorted((a,v))))
        E0=common|{tuple(sorted((u,v))) for A,B in ((Ap,Bp),(Am,Bm)) for u in A for v in B}
        E1=common|{tuple(sorted((u,v))) for A,B in ((Ap,Bm),(Am,Bp)) for u in A for v in B}
        assert not is_connected(n,E0) and is_connected(n,E1)
        for signed in (False,True):
            def sketches(E):
                out=[0]*n
                for u,v in E:
                    out[u]=(out[u]+weights[v])%p
                    out[v]=(out[v]+(-1 if signed else 1)*weights[u])%p
                return out
            assert sketches(E0)==sketches(E1)
        count+=1
result['common_additive_switch']={'instances_checked':count,'signed_and_unsigned':True}
# Previously found counterexample to a naive product-collision bound.
n=4;E=list(combinations(range(n),2))
tables=[[1,0,1,0,0,0,1,1],[0,1,1,1,0,0,0,1],[0,0,0,1,1,1,1,1],[0,0,1,0,1,0,1,1]]
def transcript(mask):
    out=[]
    for v in range(n):
        inc=[j for j,e in enumerate(E) if v in e]
        local=sum(((mask>>j)&1)<<i for i,j in enumerate(inc))
        out.append(tables[v][local])
    return tuple(out)
cuts=[sum((((s>>u)&1)^((s>>v)&1))<<j for j,(u,v) in enumerate(E)) for s in range(1<<(n-1))]
num=sum(transcript(x)==transcript(c) for x in range(1<<len(E)) for c in cuts)
assert num==27
result['naive_collision_bound_counterexample']={'numerator':num,'denominator':512,'claimed_product_bound':'1/16'}
print(json.dumps(result,indent=2))
Path(__file__).with_name('verification_results.json').write_text(json.dumps(result,indent=2)+'\n')
