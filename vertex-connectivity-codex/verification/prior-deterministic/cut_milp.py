"""Exact feasibility model for one-bit deterministic star messages recognizing cuts.
MIP encodes all good-vs-bad transcript distinctions and exact XOR auxiliaries.
"""
from itertools import combinations
import numpy as np
from scipy.optimize import milp, Bounds, LinearConstraint
from scipy.sparse import coo_matrix
import sys, json, time
n=int(sys.argv[1]) if len(sys.argv)>1 else 4
edges=list(combinations(range(n),2)); N=len(edges); q=1<<(n-1)
local=np.zeros((1<<N,n),dtype=int)
for v in range(n):
    incident=[j for j,(a,b) in enumerate(edges) if v in (a,b)]
    for k,j in enumerate(incident):local[:,v] |= ((np.arange(1<<N)>>j)&1)<<k
cuts=[]
for sm in range(1<<(n-1)):
    cuts.append(sum(((((sm>>u)&1)^((sm>>v)&1)))<<j for j,(u,v) in enumerate(edges)))
cutset=set(cuts)
pairs=list(combinations(range(q),2)); pc=len(pairs)
pair_index={p:i for i,p in enumerate(pairs)}
def x(v,a): return v*q+a
def y(v,a,b):return n*q+v*pc+pair_index[tuple(sorted((a,b)))]
V=n*q+n*pc
rr=[]; cc=[]; vv=[]; lbs=[]; ubs=[]
def add(terms,lb=-np.inf,ub=np.inf):
    i=len(lbs)
    for col,val in terms:rr.append(i);cc.append(col);vv.append(val)
    lbs.append(lb);ubs.append(ub)
for v in range(n):
    for a,b in pairs:
        i,j,k=x(v,a),x(v,b),y(v,a,b)
        add([(k,1),(i,-1),(j,1)],0)
        add([(k,1),(i,1),(j,-1)],0)
        add([(k,1),(i,-1),(j,-1)],ub=0)
        add([(k,1),(i,1),(j,1)],ub=2)
for g in cuts:
    for h in range(1<<N):
        if h in cutset:continue
        add([(y(v,local[g,v],local[h,v]),1) for v in range(n) if local[g,v]!=local[h,v]],1)
lo=np.zeros(V);hi=np.ones(V)
for v in range(n):hi[x(v,0)]=0
A=coo_matrix((vv,(rr,cc)),shape=(len(lbs),V)).tocsc()
print('n',n,'variables',V,'constraints',len(lbs),flush=True)
t=time.time(); res=milp(np.zeros(V),integrality=np.ones(V),bounds=Bounds(lo,hi),constraints=LinearConstraint(A,np.array(lbs),np.array(ubs)),options={'time_limit':40.0})
print('elapsed',time.time()-t,'status',res.status,'message',res.message,flush=True)
if res.x is not None:
    functions=np.rint(res.x[:n*q]).astype(int).reshape(n,q).tolist()
    out={'n':n,'status':int(res.status),'functions':functions}
    good={tuple(functions[v][local[g,v]] for v in range(n)) for g in cuts}
    for h in range(1<<N):
        if h not in cutset:
            assert tuple(functions[v][local[h,v]] for v in range(n)) not in good
    print(json.dumps(out),flush=True)
