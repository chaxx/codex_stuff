#!/usr/bin/env python3
"""Bounded finite experiments for workflow 01. See adjacent report for limits.
Default: exact standard-library checks plus two <=30s SciPy MILPs.
Use --skip-milp for a standard-library-only run. No random choices.
"""
from itertools import combinations
from pathlib import Path
from collections import Counter
import argparse
import json
import platform
import time


def graph_data(m):
    edges = list(combinations(range(m), 2))
    stars = []
    for x in range(1 << len(edges)):
        stars.append([sum(((x >> j) & 1) << k
                          for k, j in enumerate(i for i, e in enumerate(edges) if v in e))
                      for v in range(m)])
    cuts = {sum((((s >> u) ^ (s >> v)) & 1) << j
                for j, (u, v) in enumerate(edges))
            for s in range(1 << (m - 1))}
    return edges, stars, cuts


def exact_onebit_cut_search(m):
    """Enumerate all local Boolean maps, modulo independent output complements.

    A constraint is a cut/noncut input pair. A branch is pruned only when an
    uncovered constraint cannot be distinguished by any unassigned player.
    This requires no numerical optimization or asymptotic inference.
    """
    edges, stars, cuts = graph_data(m)
    constraints = [(c, x) for c in sorted(cuts) for x in range(1 << len(edges)) if x not in cuts]
    local_inputs = 1 << (m - 1)
    function_count = 1 << (local_inputs - 1)  # f(0)=0 without loss of generality
    missing = [[0] * function_count for _ in range(m)]
    forced = [0] * (m + 1)
    for k, (c, x) in enumerate(constraints):
        highest = max(v for v in range(m) if stars[c][v] != stars[x][v])
        for depth in range(highest + 1, m + 1):
            forced[depth] |= 1 << k
        for v in range(m):
            a, b = stars[c][v], stars[x][v]
            for f in range(function_count):
                table = f << 1
                if ((table >> a) & 1) == ((table >> b) & 1):
                    missing[v][f] |= 1 << k
    visited = [0] * (m + 1)
    answer = []

    def search(v, uncovered):
        visited[v] += 1
        if uncovered & forced[v]:
            return False
        if v == m:
            return True
        for f in range(function_count):
            answer.append(f << 1)
            if search(v + 1, uncovered & missing[v][f]):
                return True
            answer.pop()
        return False

    start = time.monotonic()
    exists = search(0, (1 << len(constraints)) - 1)
    # Check a positive witness directly, without constraint bitsets.
    if exists:
        good = {tuple((answer[v] >> stars[c][v]) & 1 for v in range(m)) for c in cuts}
        assert all(tuple((answer[v] >> stars[x][v]) & 1 for v in range(m)) not in good
                   for x in range(1 << len(edges)) if x not in cuts)
    result = dict(m=m, bits_per_vertex=1, output_complement_normalized=True,
                  normalized_protocols=function_count ** m, constraints=len(constraints),
                  exists=exists, search_nodes_by_depth=visited,
                  elapsed_seconds=time.monotonic() - start)
    if exists:
        result['truth_tables'] = answer
    return result


def candidate_rows(m, x):
    edges = list(combinations(range(m), 2))
    mat = [[0] * m for _ in range(m)]
    for j, (u, v) in enumerate(edges):
        mat[u][v] = mat[v][u] = (x >> j) & 1
    return [sum((mat[v][i] ^ mat[v][0]) << (i - 1) for i in range(1, m))
            for v in range(m)]


def anchored_example():
    # root 0, h_0(s)=s_1,h_1(s)=s_2,h_2(s)=s_3,h_3(s)=s_1.
    coordinate = [0, 1, 2, 0]
    nonroot_edges = list(combinations(range(1, 4), 2))
    checked = 0
    for s in range(8):
        for mask in range(1, 8):
            rows = [0] * 4
            for j, (u, v) in enumerate(nonroot_edges):
                if (mask >> j) & 1:
                    rows[u] ^= 1 << (v - 1)
                    rows[v] ^= 1 << (u - 1)
            assert any(((s ^ rows[v]) >> coordinate[v]) & 1 != (s >> coordinate[v]) & 1
                       for v in range(4))
            checked += 1
    def transcript(x):
        return [(s >> coordinate[v]) & 1 for v, s in enumerate(candidate_rows(4, x))]
    x = (1 << 1) | (1 << 5)  # labels 02 and 23 are one, all others zero.
    assert transcript(x) == transcript(0) == [0] * 4
    assert x not in graph_data(4)[2]
    return dict(m=4, bits=1, maps=['s1', 's2', 's3', 's1'],
                anchored_instances_checked=checked, anchored_collision=False,
                full_cut_recognition_collision={'cut_mask': 0, 'noncut_mask': x,
                                                'noncut_one_edges': [[0, 2], [2, 3]],
                                                'transcript': transcript(x)})


def rank_binary(rows):
    basis = {}
    for row in rows:
        while row:
            p = row.bit_length() - 1
            if p in basis:
                row ^= basis[p]
            else:
                basis[p] = row
                break
    return len(basis)


def lift_and_rank_checks():
    cases = 0
    by_m = {}
    for m in range(2, 7):
        edges = list(combinations(range(m), 2))
        counts = Counter()
        for x in range(1 << len(edges)):
            parent = list(range(2 * m))
            def find(a):
                while parent[a] != a:
                    parent[a] = parent[parent[a]]
                    a = parent[a]
                return a
            rows = [0] * m
            for j, (u, v) in enumerate(edges):
                label = (x >> j) & 1
                if label:
                    rows[u] |= 1 << v
                    rows[v] |= 1 << u
                for b in (0, 1):
                    a, c = find(2*u+b), find(2*v+(b ^ label))
                    parent[a] = c
            components = len({find(v) for v in range(2*m)})
            # An independent path-potential consistency predicate.
            cut = all(((rows[u] >> v) & 1) == (((rows[0] >> u) ^ (rows[0] >> v)) & 1)
                      for u, v in edges)
            assert components == (2 if cut else 1)
            rank = rank_binary(rows)
            assert rank % 2 == 0
            counts[rank] += 1
            cases += 1
        # Count ALL alternating m-by-m matrices, not just full-row support.
        # These finite inequalities are sanity checks, not a proof for all m.
        for r in range(m + 1):
            assert sum(c for rank, c in counts.items() if rank <= r) <= 2 ** (r*m)
        by_m[str(m)] = {str(rank): count for rank, count in sorted(counts.items())}
    return dict(labelings_checked=cases, m_range=[2, 6],
                method='union-find on lift vs root path potentials',
                alternating_rank_counts=by_m,
                finite_rank_count_inequality='#{D alternating m by m: rank(D)<=r} <= 2^(r*m)')


def root_zero_milp(m, limit=30.0):
    """Every h_v has one output bit; impose separation for every (s,D!=0).

    Root's output is irrelevant. Differences preserve coordinate v, so each
    h_v may be complemented independently on its s_v=0 and s_v=1 slices.
    Four standard inequalities enforce each auxiliary y = XOR(h_v(a),h_v(b)).
    A returned feasible vector is rounded and independently checked exactly.
    Infeasibility is a numerical-solver report, not a proof certificate.
    """
    import numpy as np
    import scipy
    from scipy.optimize import milp, Bounds, LinearConstraint
    from scipy.sparse import coo_matrix
    p = m - 1
    q = 1 << p
    edges = list(combinations(range(p), 2))
    pairs = [(v, a, b) for v in range(p) for a in range(q) for b in range(a+1, q)
             if not ((a ^ b) >> v) & 1]
    yi = {triple: p*q+i for i, triple in enumerate(pairs)}
    nv = p*q + len(pairs)
    rr, cc, vv, lb, ub = [], [], [], [], []
    def add(terms, lower=-np.inf, upper=np.inf):
        row = len(lb)
        for col, val in terms:
            rr.append(row); cc.append(col); vv.append(val)
        lb.append(lower); ub.append(upper)
    for (v, a, b), y in yi.items():
        i, j = v*q+a, v*q+b
        add([(y,1),(i,-1),(j,1)],0)
        add([(y,1),(i,1),(j,-1)],0)
        add([(y,1),(i,-1),(j,-1)],upper=0)
        add([(y,1),(i,1),(j,1)],upper=2)
    differences = []
    for mask in range(1, 1 << len(edges)):
        rows = [0]*p
        for j, (u,v) in enumerate(edges):
            if (mask >> j) & 1:
                rows[u] |= 1 << v; rows[v] |= 1 << u
        differences.append(rows)
        for s in range(q):
            add([(yi[(v, min(s,s^rows[v]), max(s,s^rows[v]))],1)
                 for v in range(p) if rows[v]],1)
    lo, hi = np.zeros(nv), np.ones(nv)
    for v in range(p):
        hi[v*q] = hi[v*q+(1<<v)] = 0
    a = coo_matrix((vv,(rr,cc)),shape=(len(lb),nv)).tocsc()
    start = time.monotonic()
    res = milp(np.zeros(nv), integrality=np.ones(nv), bounds=Bounds(lo,hi),
               constraints=LinearConstraint(a,np.array(lb),np.array(ub)),
               options={'time_limit':limit})
    out = dict(m=m,bits=1,anchors=q,nonzero_differences=len(differences),
               variables=nv,constraints=len(lb),scipy_version=scipy.__version__,
               time_limit_seconds=limit,status=int(res.status),message=res.message,
               elapsed_seconds=time.monotonic()-start)
    if res.x is not None:
        tables = np.rint(res.x[:p*q]).astype(int).reshape(p,q).tolist()
        assert all(any(tables[v][s] != tables[v][s^rows[v]] for v in range(p))
                   for rows in differences for s in range(q))
        out['nonroot_truth_tables'] = tables
        out['exact_witness_recheck_passed'] = True
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--skip-milp',action='store_true')
    args = ap.parse_args()
    result = {'python': platform.python_version(), 'randomness': 'none',
              'onebit_cut_exhaustive': [exact_onebit_cut_search(m) for m in (3,4)],
              'anchored_counterexample': anchored_example(),
              'lift_and_rank': lift_and_rank_checks()}
    if not args.skip_milp:
        result['root_zero_milp'] = [root_zero_milp(m) for m in (4,5)]
    path = Path(__file__).with_suffix('.json')
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
