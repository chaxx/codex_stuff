# Independent reverse audit: removing the two extra bits

Date: 2026-10-29. Reviewer: `algebraic_sketches` specialist.

## Independence and verdict

The coordinator supplied only the fresh proof auditor's proposed refinement statement. I did not read the auditor's reports or receive its proof. I independently derived the proof below, using the alternating-matrix count that I had already proved in my own original report. This is a reverse audit of a refinement I did not propose.

**Verdict: VERIFIED (complete proof).** The additive `+2` in my original theorem is unnecessary. This improves the quantitative obstruction, not the unrestricted connectivity lower bound. The original report is left unchanged as the record of the earlier proposal.

## Exact statement

For all integers `n >= 2` and `r >= 0`, there exist vertex-specific linear maps

\[
 A_v:\mathbb F_2^{n-1}\to\mathbb F_2^b,
 \qquad b=r+\lceil\log_2 n\rceil,
\]

such that every nonzero symmetric zero-diagonal binary `n x n` matrix `D` of rank at most `r` satisfies `A_v(D_v) != 0` for at least one vertex `v`. The diagonal coordinate is omitted from `D_v` when applying the map. Thus two graph inputs with a nonzero adjacency-XOR difference of rank at most `r` cannot have identical concatenated transcripts.

These are fixed-length deterministic maps, fixed after a probabilistic existence argument. Each vertex receives only its incident edge indicators. No connectivity-deciding referee or uniform efficient construction is asserted. Evaluation of a chosen dense map costs `O(nb)` binary operations per vertex. The statement is valid but trivial if its budget exceeds the full neighborhood length.

## Proof

### 1. Counting lemma

For integers `t >= 1` and `r >= 2`, at most `2^(rt)` symmetric zero-diagonal `t x t` binary matrices have rank at most `r`.

If `r >= t`, there are only `2^(t(t-1)/2) <= 2^(rt)` such matrices in total. Suppose `2 <= r < t`. Any column space of dimension at most `r` lies in an `r`-dimensional subspace `W`. Fix a basis matrix `U` of size `t x r` and a left inverse `L` of size `r x t`. Every symmetric matrix `D` with columns in `W` has

\[
 D=U C U^T,\qquad C=L D L^T.
\]

For symmetric zero-diagonal `D`, the form is alternating and so is `C`. Hence a fixed `W` allows at most `2^(r(r-1)/2)` choices. There are

\[
 {t\brack r}_2
 =2^{r(t-r)}\prod_{i=0}^{r-1}
 \frac{1-2^{i-t}}{1-2^{i-r}}
 <4\,2^{r(t-r)}
\]

possible subspaces. The denominator product `prod_{j=1}^r(1-2^(-j))` exceeds `1/4`: for `r=2` it is `3/8`; for larger `r`, the first two factors give `3/8` and the remaining product is at least `1-sum_{j=3}^r 2^(-j) > 3/4`. The numerator is at most one.

Consequently the matrix count is at most

\[
 4\,2^{r(t-r)+r(r-1)/2}
 =4\,2^{rt-r(r+1)/2}\le 2^{rt},
\]

since `r(r+1)/2 >= 3`. Lower-rank matrices may be counted for multiple `W`, which only increases this upper bound.

### 2. Random local maps and the refined union bound

Assume `r >= 2` for now. Sample all entries of all `A_v` independently and uniformly from `F_2`. For a fixed nonzero symmetric zero-diagonal `D` with `t` nonzero rows, each nonzero row is killed by its independently sampled local map with probability `2^(-b)`. Thus the probability that the entire transcript vanishes is `2^(-bt)`.

A nonzero symmetric zero-diagonal matrix has **at least two nonzero rows**, so `t >= 2`. Symmetry confines every nonzero column to the same support. Choose that support in `binom(n,t)` ways and apply the counting lemma to its principal `t x t` matrix. The union bound is

\[
 \begin{aligned}
 \Pr[\exists D\ne0:\operatorname{rank}D\le r,
                  \ A_v(D_v)=0\text{ for every }v]
 &\le\sum_{t=2}^n\binom nt 2^{(r-b)t}\\
 &\le\sum_{t=2}^n\binom nt n^{-t}\\
 &\le\sum_{t=2}^n\frac1{t!}
 <1.
 \end{aligned}
\]

The middle inequality uses `b-r=ceil(log_2 n)`. For an elementary check of the final strict bound, `t! >= 2^(t-1)` for `t >= 2`, so the finite sum is at most `sum_{t=2}^n 2^(-(t-1))=1-2^(-(n-1))<1`. Equivalently the infinite sum is `e-2<1`.

Therefore a successful choice exists. This proof retains both pieces of information discarded by the coarse geometric bound in my original report: the binomial support count and the impossibility of support size one.

### 3. Degenerate ranks

For `r=0`, a nonzero matrix cannot have rank at most `r`. For `r=1`, a nonzero symmetric zero-diagonal binary matrix contains an off-diagonal one, and its corresponding principal `2 x 2` submatrix is

\[
 \begin{pmatrix}0&1\\1&0\end{pmatrix},
\]

which has rank two. Thus rank one is also impossible. The theorem is vacuous in these two cases, and any maps of the specified length suffice.

## Adversarial checks and limitations

- All matrices are over `F_2`; zero diagonal is essential to the support and rank observations.
- Graph-row dependencies cause no invalid probability factorization: a fixed `D` is tested against independent random maps at different vertices.
- The union bound counts zero and smaller-support matrices when overcounting a chosen principal support; this is harmless.
- No asymptotic rounding issue occurs: `2^(-ceil(log_2 n)) <= 1/n` for every integer `n >= 2`.
- `r > t`, `r >= n`, and `n=2` are covered explicitly, rather than using a nonexistent `r`-subspace of `F_2^t`.
- The existence argument does not claim these short sketches decide connectivity. In particular, it cannot be used as a connectivity upper bound.
- No literature novelty or finite-test evidence is needed for this proof. The provenance is a refinement proposed by the separate auditor and independently checked here.
