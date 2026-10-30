# Deterministic connectivity research — 29 October 2026

## Outcome

**No unrestricted improvement beyond Ω(√n) was obtained.** The draft's k=1 lower bound passed a separate proof audit, with a self-contained proof and explicit constants. The clearest additional result is a sharper obstruction to low-rank collision arguments: **r+⌈log₂ n⌉ bits per vertex suffice to exclude every nonzero adjacency difference of binary rank at most r**. This improves the prior note's `2r+⌈log₂ n⌉+2` bound. It is not a connectivity protocol or a stronger unrestricted lower bound. Literature novelty is not asserted.

Four specialist tracks ran independently: new graph families, algebraic/cut-space methods, primary-source literature, and finite experiments. A fresh auditor received isolated statements, locked a blind attack, then reviewed the proposed proofs. A separate reverse audit checked the auditor's further refinement of the rank barrier. The research run preserved its inputs; a subsequent explicit user request authorized the separate dimension correction to `sources/prior-notes/vertex_connectivity_research_note.tex` documented below.

Read the [compiled mathematical note](../manuscript/lower_bound_candidate.pdf) or [LaTeX source](../manuscript/lower_bound_candidate.tex) for the selected audited results with full proofs. This is a new research note, not a replacement for the author's original manuscript.

## Model and result boundaries

There are n labeled vertices of a simple undirected graph. Vertex v knows only its own neighborhood and sends one deterministic simultaneous message to an arbitrary referee. The output is exact Boolean connectivity. B is the worst-case **maximum bits sent by one vertex**, not total communication. Encoders may be nonlinear and vertex-specific unless a restriction is explicit. There is no randomness or decoding-time assumption in the lower bound.

Fixed-length b-bit messages have at most 2^b values. Variable binary strings of length at most B have 2^(B+1)−1 possible values. All graphs retain their fixed labeled edge universes; lifts are restricted graph families, not changes to ambient sketch coordinates.

| Claim | Result | Status and scope |
|---|---|---|
| D-01, k=1 | B=Ω(√n), explicit constants below | Independently checked; arbitrary encoders/referee |
| N2-05 / R26-RANK | Rank-r differences excluded by r+⌈log₂ n⌉ local linear bits | Independently checked; proof-strategy obstruction |
| R26-CUT-LINEAR | Local binary affine-linear cut recognition has global rank ≥binom(m,2)−1 | Independently checked; restricted encoders |
| R26-ANCHOR-4 | One-bit maps at m=4 avoid every zero-root collision but fail cut recognition | Independently checked explicit counterexample |
| R26-LIFT-CEILING | Public r-lifts of H admit reconstruction with Δ(H)⌈log₂ r⌉ bits per vertex | Independently checked; promise family only |
| R26-CUT4-FINITE | No two-symbol local protocol recognizes cuts of K₄ | Exact finite enumeration, reproduced; not asymptotic |
| N2-02 | Sublinear arbitrary-map high-rank collision target | Open |
| All-k claims, N1 claims, N2-03, remaining N2-04 variants | Not established by this run | Prior status retained; no blanket promotion |

## Proved: unrestricted square-root baseline

For every n≥2, if each message alphabet has size at most 2^b for an integer b≥1, then

\[
b>\frac{n}{768(\lceil\sqrt n\rceil+1)}>\frac{\sqrt n}{2304}.
\]

Fixed-length maximum B therefore satisfies B>√n/2304; variable strings of maximum length B satisfy B>√n/4608. These conservative constants reconstruct the draft's k=1 result and are not claimed optimal.

**Proof, with the global consistency step explicit.** Put q=128(⌈√n⌉+1), M=n−q. The case b>√n is immediate. If M<4(qb+1), then n<(4b+1)q+4≤6bq, giving the bound. Otherwise q<n, so a q-vertex reservoir and M centers exist. No construction is attempted when q≥n.

Set d=16(b+1)≤q/8. For each center's arbitrary encoder f and every d-element reservoir subset Y, pair Y's elements and fix one pair's choice. Among the 2^(d/2−1)>2^(2b) sets A choosing one element from each pair, two distinct choices A₀,A₁ have the same ordered messages `(f(A), f(Y\A))`. Their intersection, outside union, and two differences form four nonempty sets P⁰,P¹,R⁰,R¹ with

\[
f(P^a\cup R^0)=f(P^a\cup R^1),\qquad a=0,1.
\]

The bad four-label reservoir partitions cannot shatter any d coordinates. A self-contained four-letter Sauer counting induction bounds their number by ∑_{j<d}binom(q,j)3^(q−j): the union U and intersection I of the four last-coordinate slices satisfy |S|≤3|U|+|I|, with shattering thresholds d and d−1. A uniform labeling is therefore bad for one center with probability at most Pr[Bin(q,1/4)<d]≤e^(−q/32). Since ne^(−q/32)<1, one partition works for every center. No independence of the bad events is assumed.

Make P₀∪R₀ and P₁∪R₁ cliques. In G(a,c), center i has neighborhood Pᵢ^(aᵢ)∪Rᵢ^(cᵢ). Centers and P vertices send messages depending only on a; R vertices send messages depending only on c. The R transcript has at most 2^(qb) values, whereas M>qb, so distinct x,y have equal R transcripts. G(x,x) and G(x,y) have identical **entire** transcripts. The former has two components; a differing center bridges both cliques in the latter. This contradicts correctness. For variable strings apply the alphabet result with b=B+1 and use B≥1 and B+1≤2B.

Full details: [lower-bound proof](agents/lower_bounds/2026-10-29-analysis.md) and [final audit](agents/proof_auditor/2026-10-29-audit.md). The auditor left the central theorem unresolved during the [blind phase](agents/proof_auditor/2026-10-29-blind.md), then verified the released proof. This is a decision lower bound; no graph-recovery information is charged to the transcript.

## Proved: sharper obstruction to low-rank witnesses

For all integers n≥2 and r≥0, there exist vertex-specific maps

\[
A_v:\mathbb F_2^{n-1}\to\mathbb F_2^b,\qquad b=r+\lceil\log_2 n\rceil,
\]

such that no nonzero symmetric zero-diagonal matrix D of rank at most r has A_v(D_v)=0 at every vertex. Here D_v omits its diagonal coordinate. The maps are fixed and deterministic; the existence proof is nonconstructive. A chosen dense map can be evaluated in polynomial time.

**Counting lemma.** On a fixed t-vertex set there are at most 2^(rt) such matrices of rank at most r. Put r′=2⌊r/2⌋. Symplectic normal form represents each as UJUᵀ, with U of size t×r′ and J a direct sum of `[[0,1],[1,0]]` blocks; pad U with zero columns for smaller rank. There are at most 2^(r′t)≤2^(rt) choices. The normal form follows by splitting off a pair with nonzero pairing and iterating on its orthogonal complement. Nonzero alternating matrices have even rank and at least two nonzero rows.

**Proof.** Choose local matrices independently and uniformly. A fixed D with exactly t nonzero rows is killed with probability 2^(−bt). Symmetry confines its nonzero columns to the same support. Thus the probability that any forbidden D is killed is at most

\[
\sum_{t=2}^n\binom nt2^{(r-b)t}
\le\sum_{t=2}^n\binom nt n^{-t}
\le\sum_{t=2}^n\frac1{t!}
\le\sum_{t=2}^n2^{-(t-1)}<1.
\]

Fix a successful choice. The independence is between sampled maps, not between rows of a random symmetric graph under fixed nonlinear encoders.

Rank-two/biclique switches can therefore all be excluded by ⌈log₂ n⌉+2 bits per vertex. For b≫log n, a universal collision lemma based **only on the bit budget** must accommodate ranks roughly b or larger for some encoders, or use another mechanism. This does not rule out arguments using additional consequences of assumed protocol correctness. These separating maps do **not** solve general connectivity; high-rank kernel differences may remain.

The algebraic specialist first improved the prior coefficient 2r to r with additive 2. The fresh auditor independently proved that statement, then removed the additive 2. The algebraic specialist independently checked the stronger statement without seeing the auditor's argument. See [original algebraic analysis](agents/algebraic_sketches/2026-10-29-analysis.md), [blind audit](agents/proof_auditor/2026-10-29-blind.md), and [reverse audit](agents/algebraic_sketches/2026-10-29-rank-constant-audit.md).

## Proved: local linear cut recognition

Let C_m={δs:s∈F₂^m}, `(δs)uv=s_u+s_v`, be the cut space of K_m, m≥3. Binary affine-linear star messages permitting exact recognition by any referee have concatenated linear rank at least binom(m,2)−1. Thus fixed-length messages satisfy ∑_v B_v≥binom(m,2)−1 and B≥⌈(binom(m,2)−1)/m⌉.

**Proof.** Remove affine constants and let K be the global kernel. Correctness forces K⊆C_m, since zero is a cut. If K contained independent cuts δa,δb, gauge a₁=b₁=0 and put D_uv=a_u b_v+b_u a_v. At vertex v, D_v=a_v(δb)_v+b_v(δa)_v, so every local map kills it. But D is nonzero, symmetric, zero-diagonal, and has zero root row; the only cut with zero root row is zero. Contradiction. Hence dim K≤1. Nonlinear fibers are not kernels, so this proof does not extend to the unrestricted target. The [auditor](agents/proof_auditor/2026-10-29-audit.md) also checked rank sharpness, without claiming sharp maximum communication for every m.

## Proved: limits on two proposed hard families

**Anchored collisions at m=4.** With root 0 and s=(0,s₁,s₂,s₃), let `(h₀,h₁,h₂,h₃)=(s₁,s₂,s₃,s₁)`. Preserving all messages under s→s+D_v for zero-root D forces D₁₂=D₂₃=D₃₁=0, and the root condition forces the other edges to zero. No nonzero anchored collision exists, for any s.

Nevertheless under P_v(x)_i=x_vi+x_v0 the actual transcript is

\[
(x_{01},x_{12}+x_{10},x_{23}+x_{20},x_{31}+x_{30}).
\]

The zero cut and the labeling with ones exactly on 02 and 23 both give transcript zero; triangle 012 shows the latter is a noncut. Avoiding anchored collisions does not prove cut-recognition correctness. This finite example does **not** refute the asymptotic sublinear-bit target.

**Public many-sheet lifts.** Fix a public labeled base H and r≥2. Every lifted vertex `(v,a)` can send the sheet index of its unique neighbor in each public adjacent fiber. This reconstructs the entire standard r-sheet lift with Δ(H)⌈log₂ r⌉ maximum bits and polynomial decoding. For H=K_m, n=mr, the cost is `(m−1)⌈log₂ r⌉=O((n/r)log r)`. To rule out Ω(n/log^C n) from this family, it suffices that r/log r=ω(log^C n); r≥√n gives O(√n log n). Unknown fiber labels define a different family. Both propositions have full independent proofs in the [blind audit](agents/proof_auditor/2026-10-29-blind.md).

## Candidate / conditional and open

The two-lift reduction itself is valid: a binary labeling of K_m produces two disjoint m-cliques if it is a cut, and a connected lift otherwise. A base player can simulate its two lifted vertices using only its star. The exact factor-two relation `D_conn(2m)≥D_cut(m)/2` uses fixed-length/log-alphabet cost; variable strings of maximum length B can safely be simulated with 2(B+1) fixed bits. Raw concatenation need not be parseable. The [final audit](agents/proof_auditor/2026-10-29-audit.md) checked this framing correction and the lift lemma.

What remains missing is a simultaneous high-rank collision theorem for **arbitrary, different nonlinear local maps**. Large fibers, common-map affine-plane arguments, and translation-invariance of linear kernels do not supply it. The zero-root condition is sufficient for the reduction but stronger than necessary. A normal-form theorem converting arbitrary short messages to linear, mergeable, low-degree, or low-alternation messages would itself require proof.

The abstract's all-k Ω(k+√n) statement is not established here. It differs from §6's Ω(n/(√n+k)); both formulas were checked visually against the original PDF. Only k=1 was audited. This is a scope discrepancy to resolve, not a refutation of the stronger theorem.

## Refuted templates and gaps

| Inference | Finding |
|---|---|
| Every one-bit family at m=4 has a zero-root collision | False: the projection maps above exclude all such collisions |
| Excluding zero-root collisions proves cut-recognition correctness | False: the same maps have a non-anchored cut/noncut collision |
| The bit budget alone guarantees bounded-rank collisions for all encoders | False in the proved rank-barrier parameter range; additional correctness assumptions are a separate possibility |
| Increasing sheets on a public base can force arbitrary near-linear cost | Limited by the exact reconstruction protocol; retain its log r factor |
| Arbitrary nonlinear collisions translate like kernel vectors | Unsupported; their base point matters |
| Two-party edge-partition bounds transfer directly to vertex-local SMP | Unsupported without a valid locality-preserving simulation and cost accounting |
| Small-n tests or numerical infeasibility prove the asymptotic target | Invalid; retain the precise finite universes and solver limitations |

## Finite verification

| Check | Universe and outcome | Status |
|---|---|---|
| Cut recognition, m=3, two symbols | 512 normalized encoder tuples; feasible | Exact, witness rechecked |
| Cut recognition, m=4, two symbols | 128⁴=268,435,456 tuples; 448 constraints; no protocol | Exact search; 499,841 nodes with sound pruning; Python/C++ agree |
| Explicit m=4 anchored example | 8 anchors ×7 differences | All 56 checks passed; also independently proved |
| m=5 anchored one-bit MILP | 16 anchors ×63 differences; 288 variables; 1,904 constraints | Solver reports infeasible in about 10 seconds; no proof certificate |
| Two-lift dichotomy | All 33,866 labelings, 2≤m≤6 | Passed; finite support for the general proof |
| Alternating matrix ranks | All matrices, 2≤m≤6 | Even ranks and count bound checked; finite evidence |
| Alternative full K₄ one-hot MILP | 30-second cap | Timeout without incumbent; inconclusive |

The two-symbol exclusion does not cover the three strings `empty`, `0`, `1` under a maximum-length-one convention. Balanced edge ownership gives a two-fixed-bit protocol on K₄, so its exact finite fixed-length cut-recognition cost is two. This does not improve the asymptotic connectivity bound.

The coordinator inspected normalization/pruning and reproduced the m=3,4 searches, 56 anchor checks, and all 33,866 lift/rank checks. See [experiment report](agents/experiments/2026-10-29-report.md), [full results](../verification/new/run_20261029_checks.json), and [coordinator reproduction](COORDINATOR-RECHECK-2026-10-29.json).

Reproduce from the workspace root:

```sh
OPENBLAS_NUM_THREADS=1 python verification/new/run_20261029_checks.py
g++ -std=c++17 -O3 verification/new/run_20261029_cut_exhaustive.cpp -o /tmp/run_20261029_cut_exhaustive
timeout 30 /tmp/run_20261029_cut_exhaustive
```

SciPy is needed for the two 30-second-capped MILPs. `--skip-milp` needs only Python's standard library, but rewrites the adjacent JSON without MILP results; preserve recorded results when comparing. The coordinator's reproduction did not overwrite the specialist's evidence.

## Literature boundary

The strongest external unrestricted deterministic bound located and source-checked in the bounded search is **Ω(n^(1/3))**, Robinson–Tan, [arXiv:2609.05795v1](https://arxiv.org/abs/2609.05795v1), submitted 5 September 2026, Theorem 1 and Corollary 1. Its vertex-local simultaneous model and maximum-message convention match this task. The draft's Ω(√n) now has an internal independent audit; publication priority is separate.

[Zhang's October 2026 result](https://arxiv.org/abs/2610.32346v1) concerns two-party disjoint edge sets and total communication. [Roughgarden–Vassilvitskii–Wang Theorem 5.3](https://timroughgarden.org/papers/mr.pdf) concerns real-field polynomial degree; its integer top coefficient can vanish in finite characteristic. [AGM](https://people.cs.umass.edu/~mcgregor/papers/12-dynamic.pdf) confirms the fixed binom(n,2)-coordinate convention. The [literature report](agents/literature/2026-10-29-review.md) records checked models, dates, primary sources, and search limits. These external statements were source-checked, not independently reproved. No exhaustive novelty certification is claimed.

## Next steps

1. Attack the full cut/noncut collision condition, explicitly allowing root-row changes and their candidate-coordinate correction. Compare it with the stronger anchored condition.
2. Seek nonlinear global consistency that permits high-rank differences; a better rank-two pigeonhole argument cannot overcome the audited barrier for arbitrary vertex-specific maps.
3. Obtain a checkable certificate or structural human proof for the m=5 anchored solver result. More solver time alone does not address the asymptotic problem.
4. Consider constant-sheet dense lifts or hidden partitions, checking their description cost before changing the sheet count or public template.
5. Resolve the all-k manuscript discrepancy in a separate audit; do not extend the k=1 verdict to unrelated claims.

## Separate user-requested dimension correction

The user subsequently requested an edit to [vertex_connectivity_research_note.tex](../sources/prior-notes/vertex_connectivity_research_note.tex). That explicit request authorizes this source exception. The revised rank lemma keeps the entire original edge universe N=binom(n,2):

\[
M=BW\Psi^{\mathsf T},\qquad B:r\times N,\quad W:N\times N,
\quad\Psi:t\times N,\quad M:r\times t.
\]

It defines the locally computable transformed sketch, preserves original edge identities through row aggregation, and distinguishes the raw vertex-indexed Vandermonde matrix (n columns) from the transformed edge map (N columns). The smaller B_S,W_S,Ψ_S occur only in the rank proof. Full W may have zero failed-endpoint weights; only W_S on surviving active edges is inverted. The constant-field variant similarly states M=BK with dimensions (r×N)(N×D)=r×D.

The changed algebra was separately checked: [dimension audit](agents/proof_auditor/2026-10-29-dimensions.md). See the [edit/build report](agents/algebraic_sketches/2026-10-29-dimension-correction.md), [compiled corrected note](dimension-correction/vertex_connectivity_research_note.pdf), and [patch](dimension-correction/dimension-correction.patch). The original draft and the uploaded prior-note PDF are preserved; the corrected PDF is a separate output. This edit does not promote the prior note's unrelated theorem claims.

## Run record and audit provenance

- [Workflow](../workflows/01-deterministic-connectivity.md), [archive/source hashes](RUN-2026-10-29.json), [claim ledger](../context/claims.md), [issues](../context/issues.md).
- [Lower bounds](agents/lower_bounds/2026-10-29-analysis.md), [algebraic approach](agents/algebraic_sketches/2026-10-29-analysis.md), [literature](agents/literature/2026-10-29-review.md), [experiments](agents/experiments/2026-10-29-report.md).
- [Locked blind audit](agents/proof_auditor/2026-10-29-blind.md), [released-proof audit](agents/proof_auditor/2026-10-29-audit.md), [rank reverse audit](agents/algebraic_sketches/2026-10-29-rank-constant-audit.md), [manuscript compilation](agents/manuscript_editor/2026-10-29-report.md).
- The first auditor inherited proof-containing context, flagged it, and aborted without issuing a mathematical verdict. Its [provenance note](agents/proof_auditor/2026-10-29-aborted-inherited-context.md) is preserved. All independent verdicts use the replacement launched with no inherited history, or the documented reverse audit.
- Native collaboration tools executed the supplied role definitions; no nested Codex CLI invocation was needed. No external expensive compute/API run or author acceptance is implied. The sole source-edit exception is the user's separately requested dimension correction, with input and final hashes recorded.
