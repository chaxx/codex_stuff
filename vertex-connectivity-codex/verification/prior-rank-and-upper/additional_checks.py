"""Finite checks of the constant-field rank protocol and near-complete regime.
These are reproducible sanity checks, not proofs or independent-agent reviews.
"""
from itertools import combinations, product
import json
import random
import time
import networkx as nx
from checks import graph, rank_mod, partition


def nullspace_mod(rows, columns, p):
    a = [[x % p for x in row] for row in rows]
    pivots = []
    rank = 0
    for j in range(columns):
        pivot = next((i for i in range(rank, len(a)) if a[i][j]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        inv = pow(a[rank][j], -1, p)
        a[rank] = [x * inv % p for x in a[rank]]
        for i in range(len(a)):
            if i != rank and a[i][j]:
                factor = a[i][j]
                a[i] = [(x-factor*y) % p for x,y in zip(a[i], a[rank])]
        pivots.append(j)
        rank += 1
        if rank == len(a):
            break
    basis = []
    for j in range(columns):
        if j not in pivots:
            x = [0] * columns
            x[j] = 1
            for i, pivot in enumerate(pivots):
                x[pivot] = -a[i][j] % p
            basis.append(x)
    return basis


def dot(a,b,p):
    return sum(x*y for x,y in zip(a,b)) % p


def rank_protocol_checks():
    rng = random.Random(20261029)
    p = 5
    trials = exact = deficient = identities = 0
    inputs = []
    for n in (3,4):
        edges = list(combinations(range(n),2))
        for mask in range(1 << len(edges)):
            inputs.append(graph(n,[e for i,e in enumerate(edges) if mask >> i & 1]))
    n = 7
    edges = list(combinations(range(n),2))
    for _ in range(60):
        prob = rng.random()
        inputs.append(graph(n,[e for e in edges if rng.random()<prob]))
    for G in inputs:
        n = len(G)
        for k in range(1, min(n,4)):
            for b in (1,2):
                J = graph(n, [])
                s = b+k-1
                for v in G:
                    J.add_edges_from((v,u) for u in sorted(G[v])[:s])
                for size in range(k):
                    for Ftuple in combinations(range(n),size):
                        F = set(Ftuple)
                        keep = set(G)-F
                        Gf, Jf = G.subgraph(keep), J.subgraph(keep)
                        components = list(nx.connected_components(Jf))
                        r = len(components)
                        c = nx.number_connected_components(Gf)
                        h = r-c
                        owner = {v:i for i,C in enumerate(components) for v in C}
                        assert h <= n/(b+1)
                        for D in (1,2,3):
                            m = D+k-1
                            for zero in (False, True):
                                Phi = [[0 if zero else rng.randrange(p) for _ in range(n)] for _ in range(m)]
                                constraints = [[Phi[t][f] for t in range(m)] for f in sorted(F)]
                                P = nullspace_mod(constraints,m,p)[:D]
                                assert len(P)==D
                                cols = [[Phi[t][v] for t in range(m)] for v in range(n)]
                                z = [[dot(P[t],cols[v],p) for v in range(n)] for t in range(D)]
                                raw = {v:[sum((1 if u>v else -1)*Phi[t][u] for u in G[v])%p for t in range(m)] for v in G}
                                M = []
                                for C in components:
                                    row=[]
                                    for t in range(D):
                                        transformed=sum(z[t][v]*dot(P[t],raw[v],p) for v in C)%p
                                        direct=sum((1 if u>v else -1)*z[t][v]*z[t][u] for v in C for u in Gf[v] if u not in C)%p
                                        assert transformed==direct
                                        identities+=1
                                        row.append(transformed)
                                    M.append(row)
                                rank=rank_mod(M,p)
                                assert rank<=h
                                assert rank != r-1 or c==1
                                if rank==h: exact+=1
                                else: deficient+=1
                                K=nullspace_mod([[M[i][t] for i in range(r)] for t in range(D)],r,p)
                                signatures=[tuple(x[i] for x in K) for i in range(r)]
                                realowner={v:i for i,C in enumerate(nx.connected_components(Gf)) for v in C}
                                representatives=[next(iter(C)) for C in components]
                                for i,j in combinations(range(r),2):
                                    if signatures[i]==signatures[j]:
                                        assert realowner[representatives[i]]==realowner[representatives[j]]
                                    if rank==h:
                                        assert (signatures[i]==signatures[j]) == (realowner[representatives[i]]==realowner[representatives[j]])
                                trials+=1
    return {'matrix_cases':trials,'rank_exact_cases':exact,'rank_deficient_cases':deficient,'transformation_identities':identities}


def polynomial_checks():
    # Exhaust all simple graphs and every 0/1 cut on 3 vertices. A nonzero
    # cut polynomial over F_5 vanishes on at most 2/5 of all assignments.
    n,p=3,5
    edges=list(combinations(range(n),2))
    count=0
    maxzeros=0
    for mask in range(1<<len(edges)):
        es=[e for i,e in enumerate(edges) if mask>>i&1]
        for x in product(range(2),repeat=n):
            coeff=[(x[u]-x[v])%p for u,v in es]
            if not any(coeff): continue
            zeros=0
            for z in product(range(p),repeat=n):
                value=sum(c*z[u]*z[v] for (u,v),c in zip(es,coeff))%p
                zeros+=(value==0)
            assert 5*zeros<=2*p**n
            maxzeros=max(maxzeros,zeros)
            count+=1
    return {'nonzero_cut_polynomials':count,'assignments_per_polynomial':p**n,'maximum_zero_assignments':maxzeros}


def near_complete_checks():
    checked=0
    for n in (3,4,5):
        es=list(combinations(range(n),2))
        for mask in range(1<<len(es)):
            G=graph(n,[e for i,e in enumerate(es) if mask>>i&1])
            actual=nx.node_connectivity(G)>=n-2
            assert actual==(min(dict(G.degree()).values())>=n-2)
            checked+=1
    return {'one_bit_threshold_graphs':checked}

def essential_edge_checks():
    tested=0
    for n in (3,4,5):
        es=list(combinations(range(n),2))
        for mask in range(1<<len(es)):
            G=graph(n,[e for i,e in enumerate(es) if mask>>i&1])
            k=max(1,max(dict(G.degree()).values()))
            for u,v in G.edges:
                F=set(G[v])-{u}
                assert len(F)<k and u not in F and v not in F
                H=G.copy(); H.remove_edge(u,v)
                keep=set(G)-F
                assert partition(G.subgraph(keep)) != partition(H.subgraph(keep))
                tested+=1
    return {'edge_indispensability_cases':tested}


if __name__=='__main__':
    start=time.time()
    results={'status':'PASS','note':'Finite checks; not an independent-agent review.'}
    for name,fn in [('constant_field_rank',rank_protocol_checks),('cut_polynomial',polynomial_checks),('near_complete',near_complete_checks),('essential_edges',essential_edge_checks)]:
        results[name]=fn()
        print(name,results[name],flush=True)
    results['elapsed_seconds']=round(time.time()-start,2)
    from pathlib import Path
    Path(__file__).with_name('additional_check_results.json').write_text(json.dumps(results,indent=2))
    print(json.dumps(results,indent=2))
