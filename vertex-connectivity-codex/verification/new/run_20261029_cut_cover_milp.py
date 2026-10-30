from itertools import combinations
import time,json
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import coo_matrix
for n in [3,4]:
 edges=list(combinations(range(n),2));q=1<<(n-1)
 stars=[]
 for g in range(1<<len(edges)):
  stars.append([sum(((g>>j)&1)<<k for k,j in enumerate(i for i,e in enumerate(edges) if v in e)) for v in range(n)])
 cuts={sum((((s>>u)&1)^((s>>v)&1))<<i for i,(u,v) in enumerate(edges)) for s in range(1<<(n-1))}
 constraints=[(c,x) for c in sorted(cuts) for x in range(1<<len(edges)) if x not in cuts]
 nt=1<<(q-1);rr=[];cc=[];vv=[]
 for v in range(n):
  for f in range(nt):rr.append(v);cc.append(v*nt+f);vv.append(1)
 for ri,(c,x) in enumerate(constraints,n):
  for v in range(n):
   a,b=stars[c][v],stars[x][v]
   for f in range(nt):
    if (((f<<1)>>a)^((f<<1)>>b))&1:rr.append(ri);cc.append(v*nt+f);vv.append(1)
 A=coo_matrix((vv,(rr,cc)),shape=(n+len(constraints),n*nt)).tocsc()
 lo=np.ones(n+len(constraints));hi=np.full(n+len(constraints),np.inf);hi[:n]=1
 t=time.monotonic();r=milp(np.zeros(n*nt),integrality=np.ones(n*nt),bounds=Bounds(0,1),constraints=LinearConstraint(A,lo,hi),options={'time_limit':30.0})
 print(n,r.status,r.message,'sec',time.monotonic()-t,flush=True)
 if r.x is not None:
  print([int(np.argmax(r.x[v*nt:(v+1)*nt]))<<1 for v in range(n)],flush=True)
