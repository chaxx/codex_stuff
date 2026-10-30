"""Finite checks of proposed lemmas; not a proof or an independent-agent review."""
from itertools import combinations
import json, random, time
import networkx as nx


def rank_mod(rows, p):
    if not rows:
        return 0
    a = [[v % p for v in row] for row in rows]
    r = 0
    for j in range(len(a[0])):
        pivot = next((i for i in range(r, len(a)) if a[i][j]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        inv = pow(a[r][j], -1, p)
        a[r] = [(v*inv) % p for v in a[r]]
        for i in range(r+1, len(a)):
            if a[i][j]:
                v = a[i][j]
                a[i] = [(x-v*y) % p for x,y in zip(a[i],a[r])]
        r += 1
        if r == len(a):
            break
    return r


def graph(n, edges):
    g = nx.Graph()
    g.add_nodes_from(range(n))
    g.add_edges_from(edges)
    return g


def partition(g):
    return frozenset(frozenset(c) for c in nx.connected_components(g))


def rank_checks():
    # All pairs H subset G on four vertices, all failure sets of size <=2,
    # and moment dimensions D=1,2,3. Also verify the moment transformation.
    n, p, labels = 4, 101, [2,3,5,7]
    es = list(combinations(range(n),2))
    failures = [set(f) for z in range(3) for f in combinations(range(n),z)]
    tests = sparse_tests = transform_tests = 0
    for ternary in range(3**len(es)):
        x = ternary; ge=[]; he=[]
        for e in es:
            t=x%3; x//=3
            if t: ge.append(e)
            if t==2: he.append(e)
        G,H=graph(n,ge),graph(n,he)
        raw={v:[sum((1 if u>v else -1)*pow(labels[u],t,p) for u in G[v])%p for t in range(5)] for v in G}
        for F in failures:
            J=G.subgraph(set(G)-F)
            Hf=H.subgraph(set(H)-F)
            cs=list(nx.connected_components(Hf)); owner={v:i for i,c in enumerate(cs) for v in c}
            ctrue=nx.number_connected_components(J)
            weights={v:1 for v in G}
            coeff=[1]
            for f in sorted(F):
                b=[0]*(len(coeff)+1)
                for i,v in enumerate(coeff):
                    b[i]=(b[i]-labels[f]*v)%p; b[i+1]=(b[i+1]+v)%p
                coeff=b
            for v in G:
                for f in F: weights[v]=weights[v]*(labels[v]-labels[f])%p
            cross=[(u,v) for u,v in J.edges if owner[u]!=owner[v]]
            for D in (1,2,3):
                rows=[]
                for C in cs:
                    row=[]
                    for t in range(D):
                        direct=sum((1 if u>v else -1)*pow(labels[u]*labels[v],t,p)*weights[u]*weights[v] for v in C for u in J[v] if u not in C)%p
                        transformed=sum(pow(labels[v],t,p)*weights[v]*sum(coeff[i]*raw[v][t+i] for i in range(len(coeff))) for v in C)%p
                        assert direct==transformed, ('moment identity',G.edges,F,C,t)
                        transform_tests+=1; row.append(direct)
                    rows.append(row)
                r=rank_mod(rows,p)
                assert r<=len(cs)-ctrue, ('false rank', ge,he,F,D,r)
                if r==len(cs)-1:
                    assert ctrue==1, ('false positive',ge,he,F,D)
                if len(cross)<=D:
                    assert r==len(cs)-ctrue, ('sparse equality',ge,he,F,D)
                    sparse_tests+=1
                tests+=1
    return {'matrix_cases':tests,'sparse_exact_rank_cases':sparse_tests,'moment_coordinates_checked':transform_tests}


def indexing_graph(s, bits, i, j, extra_pair=0, padding=0, universal=0):
    X=[('x',z) for z in range(s)]; Y=[('y',z) for z in range(s)]
    Xp=[('xp',z) for z in range(s)]; Yp=[('yp',z) for z in range(s)]
    a,b=('a',0),('b',0)
    L=X+Yp+[a,('bufferL',0)]+[('extraL',z) for z in range(extra_pair)]+[('pad',z) for z in range(padding)]
    R=Y+Xp+[b,('bufferR',0)]+[('extraR',z) for z in range(extra_pair)]
    g=nx.Graph(); g.add_nodes_from(L+R)
    g.add_edges_from(combinations(L,2)); g.add_edges_from(combinations(R,2))
    g.add_edges_from((X[z],Xp[z]) for z in range(s)); g.add_edges_from((Y[z],Yp[z]) for z in range(s))
    g.add_edges_from((X[z],Y[w]) for z in range(s) for w in range(s) if bits>>(z*s+w)&1)
    g.add_edge(a,Xp[i]); g.add_edge(b,Yp[j])
    g.add_edges_from((('extraL',z),('extraR',z)) for z in range(extra_pair))
    for z in range(universal):
        u=('universal',z); vs=list(g); g.add_node(u); g.add_edges_from((u,v) for v in vs)
    return g,2*s+1+extra_pair+universal,X+Y


def indexing_checks():
    tests=0
    for s in (1,2):
        for bits in range(1<<(s*s)):
            for extra in (0,1):
                for pad,univ in ((0,0),(2,1)):
                    neighborhoods={}
                    for i in range(s):
                        for j in range(s):
                            g,k,alice=indexing_graph(s,bits,i,j,extra,pad,univ)
                            actual=nx.node_connectivity(g)>=k
                            assert actual==bool(bits>>(i*s+j)&1), ('INDEX',s,bits,i,j,extra,pad,univ)
                            for v in alice:
                                N=frozenset(g[v])
                                assert v not in neighborhoods or neighborhoods[v]==N, 'Alice input depends on index'
                                neighborhoods[v]=N
                            tests+=1
    return {'index_gadgets_checked':tests}


def sparsify(G,k):
    H=graph(len(G),[]); queries=adds=0
    for u,v in combinations(G.nodes,2):
        while not H.has_edge(u,v):
            F=nx.minimum_node_cut(H,u,v)
            if len(F)>=k:
                break
            queries+=1
            J=G.subgraph(set(G)-set(F)); K=H.subgraph(set(H)-set(F))
            if not nx.has_path(J,u,v):
                break
            owner={x:i for i,c in enumerate(nx.connected_components(K)) for x in c}
            path=nx.shortest_path(J,u,v)
            e=next((a,b) for a,b in zip(path,path[1:]) if owner[a]!=owner[b])
            assert G.has_edge(*e) and not H.has_edge(*e)
            H.add_edge(*e); adds+=1
    assert adds<=k*len(G)-k*(k+1)//2
    assert queries<=len(G)*(len(G)-1)//2+adds
    for f in range(k):
        for F in combinations(G.nodes,f):
            keep=set(G)-set(F)
            assert partition(G.subgraph(keep))==partition(H.subgraph(keep)), ('certificate',list(G.edges),k,list(H.edges),F)
    return queries,adds


def sparsifier_checks():
    tests=queries=adds=0
    n=4; es=list(combinations(range(n),2))
    for mask in range(1<<len(es)):
        G=graph(n,[e for j,e in enumerate(es) if mask>>j&1])
        for k in range(1,n):
            q,a=sparsify(G,k); tests+=1; queries+=q; adds+=a
    rng=random.Random(20261028)
    for z in range(100):
        n=5; G=graph(n,[e for e in combinations(range(n),2) if rng.random()<rng.random()])
        for k in range(1,n):
            q,a=sparsify(G,k); tests+=1; queries+=q; adds+=a
    return {'graphs_and_thresholds_checked':tests,'oracle_queries':queries,'edges_added':adds}


if __name__=='__main__':
    start=time.time()
    result={'status':'PASS','note':'Finite checks only; no independent research agent was available.'}
    for name,fn in [('rank',rank_checks),('indexing',indexing_checks),('sparsifier',sparsifier_checks)]:
        result[name]=fn(); print(name,result[name],flush=True)
    result['elapsed_seconds']=round(time.time()-start,2)
    from pathlib import Path
    Path(__file__).with_name('check_results.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))
