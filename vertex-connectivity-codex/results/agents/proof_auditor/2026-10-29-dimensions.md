# Narrow audit of fixed-edge matrix correction — 2026-10-29

**Verdict: VERIFIED for the edited dimensions, factorizations, and rank inferences, under the explicitly stated distinct-label and distinct-edge-product assumptions. No algebraic gap found in these passages.**

This is an independent edit review, not a blind new-theorem audit. Reviewed only the matrix correction in `sources/prior-notes/vertex_connectivity_research_note.tex`, lines 62–118 and 186–190, with enough adjacent definitions to interpret it. Compared the raw and transformed sketches with Section 4 of the source draft, `sources/draft/paper-body.txt`, physical file lines 145–240 (printed manuscript lines 105–147). No source file was edited by this auditor. No verdict on the note's other claims is supplied.

## Deterministic transformed sketch

The ambient edge universe is the fixed set `E=binom([n],2)` of size `N=binom(n,2)`. The corrected matrices have compatible dimensions:

| Matrix | Dimensions | Meaning |
|---|---|---|
| Raw vertex-indexed Vandermonde map | `(2d+k+1) x n` | Maps the signed neighborhood vector to the stored raw sketch |
| `mathcal B_F` | `(n-|F|) x N` | Original-edge incidence columns; absent and failed-edge columns are zero |
| `R` | `r x (n-|F|)` | Sums surviving vertices in each component of the known spanning subgraph |
| `B=R mathcal B_F` | `r x N` | Aggregate incidence; internal columns cancel, parallel original edges remain distinct |
| `W` | `N x N` | Diagonal weights `P_F(a_u)P_F(a_v)` for every original potential edge |
| Transformed `Psi` | `t x N` | Edge-product Vandermonde columns, with `t=2d+k-|F|+1` |
| `M=BW Psi^T` | `r x t` | Aggregated transformed messages |

The raw sketch uses `epsilon_(v,u)=+1` for `v<u` and `-1` for `v>u`, matching the draft's displayed raw formula `sgn(u-v)` and its stated incidence orientation. Expanding the corrected transform gives

`a_v^j P_F(a_v) sum_l beta_l s(v)_(j+l)`

`= sum_(u in N(v)) epsilon_(v,u) P_F(a_v)P_F(a_u)(a_v a_u)^j`.

Terms at failed endpoints vanish. The largest raw coordinate accessed is `(t-1)+|F|=2d+k`, so the transformation uses exactly available coordinates. The formula yields the stated full-edge factorization, without requiring the coordinator to know the graph. Using one orientation consistently is essential; the corrected formulas do so.

The contracted multigraph represented by the nonzero columns of `B` has `r` vertices and `c` components, including isolated vertices. Its incidence rank is `r-c`; distinct parallel columns do not change this fact. Therefore `rank M<=rank B=r-c`, with no invertibility claim about the full `W`.

For the equality case, let `S` be exactly the surviving edges between distinct components of the known spanning subgraph and `m=|S|`. All other columns of `B` vanish. Consequently

`M=B_S W_S Psi_S^T`,

with dimensions `(r x m)(m x m)(m x t)`. This is an analytic support restriction, not a change to the protocol's edge universe. On surviving edges, distinct vertex labels make every diagonal entry of `W_S` nonzero. For `m<=d`, pairwise distinct edge-product labels and `t>=2d+1` give full column rank to `Psi_S`; this also follows from the invoked sparse-recovery guarantee. Thus `W_S Psi_S^T` has full row rank and a right inverse `T_S` of size `t x m`. The identity `M T_S=B_S` proves the reverse rank inequality. The `m=0` boundary is explicitly and correctly handled.

## Constant-field paragraph

The changed paragraph uses the same fixed-edge incidence matrix `B` over `F_5`. Defining `K_( {u,v},j)=z_j(u)z_j(v)` gives `K` dimensions `N x D` and

`M=BK`, with dimensions `(r x N)(N x D)=r x D`.

The identity follows directly from cancellation of each internal edge's two opposite oriented contributions. It is valid for every outcome of the public randomness, regardless of any probabilistic full-rank claim elsewhere. Hence each column of `M` lies in `im B`, and `rank M<=dim(im B)=r-c`.

The vertex-indexed random matrix `Phi` remains `m x n`. It is correctly distinguished from both the aggregate edge-incidence matrix and `K`; its `n` columns do not shrink or redefine the original `N` edge coordinates.

This audit does not certify the surrounding protocol's probability bounds, communication estimates, literature claims, or other theorems. It certifies the requested dimensional and algebraic correction only.
