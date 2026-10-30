# CLAIM LEDGER — current evidence and audit scope

Status vocabulary: ORIGINAL_DRAFT (not checked here); PROPOSED (prior AI note); IN_AUDIT; CONDITIONAL; REFUTED; VERIFIED_BY_CURRENT_AGENT (not independent); INDEPENDENTLY_CHECKED; COMPUTATION_CHECKED (explicit finite universe, no asymptotic inference); ACCEPTED_BY_AUTHOR. No prior work is automatically marked independently checked. An audit is not author acceptance.

| ID | Source | Claim / issue | Current status | Action / evidence |
|---|---|---|---|---|
| D-01 | Original draft §6 | Arbitrary deterministic connectivity B=Ω(√n), k=1 only | INDEPENDENTLY_CHECKED | Full self-contained proof, explicit constants and variable-length handling; [record](../results/claims/D-01.md). No all-k promotion |
| D-02 | Original draft §4 | Annihilator/polynomial vertex-deletion sketch | ORIGINAL_DRAFT | Fix indices, signs, field evaluation and dimensions |
| N1-01 | Prior note §3 | One-sided public rank decision sketch O(√(n log n)+k log(en/k)) | PROPOSED | Independent algebra and probability proof |
| N1-02 | Prior note §4 | Polynomial-time construction of O(kn)-edge strong certificates from forest oracle | PROPOSED | Verify oracle use, deletion sets, extremal count |
| N1-03 | Prior note | Deterministic Ω(k+√n) and randomized Ω(k+log³ n) decision lower bounds | PROPOSED | Verify reductions and literature |
| N1-04 | Prior note | Private/public log refinements and one-sided private decision | PROPOSED | Verify bounds and actual communication |
| N2-01 | Deterministic note | Two-sheeted lift: connectivity iff voltage label outside cut space | INDEPENDENTLY_CHECKED | Dichotomy and local simulation audited; exact factor 2 uses fixed/log-alphabet cost; [record](../results/claims/N2-01.md) |
| N2-02 | Deterministic note | Symmetric-collision target for arbitrary nonlinear encoders | CONDITIONAL | Still open; m=4 anchored example does not refute asymptotic target; [record](../results/claims/N2-02.md) |
| N2-03 | Deterministic note | Average-alternation and F₂-degree budgets | PROPOSED | Verify and determine sharp consequences |
| N2-04 | Deterministic note | Linear, XOR-mergeable, and common additive sketch Ω(n) bounds | PROPOSED | Check scope and exchange argument |
| N2-05 | Deterministic note + 2026-10-29 refinement | Bounded-rank switching barrier, strengthened to r+⌈log₂ n⌉ bits | INDEPENDENTLY_CHECKED | Blind audit plus independent reverse audit; budget-only universal collision templates; [record](../results/claims/N2-05.md) |
| R26-CUT-LINEAR | 2026-10-29 algebraic analysis | Local binary affine-linear cut recognition has concatenated rank ≥binom(m,2)−1 | INDEPENDENTLY_CHECKED | Restricted encoders, arbitrary referee; [record](../results/claims/R26-CUT-LINEAR.md) |
| R26-ANCHOR-4 | 2026-10-29 experiments | Explicit m=4 one-bit maps exclude all zero-root collisions but fail cut recognition | INDEPENDENTLY_CHECKED | Direct independent proof; finite counterexample only; [record](../results/claims/R26-ANCHOR-4.md) |
| R26-LIFT-CEILING | 2026-10-29 lower-bound analysis | Public r-lifts of H reconstructible with Δ(H)⌈log₂ r⌉ bits per vertex | INDEPENDENTLY_CHECKED | Exact promise-family protocol; [record](../results/claims/R26-LIFT-CEILING.md) |
| R26-CUT4-FINITE | 2026-10-29 exhaustive searches | Fixed two-symbol cut recognition on K₄ is impossible; exact fixed-length cost is 2 bits | COMPUTATION_CHECKED | Entire 128⁴ normalized truth-table universe; Python/C++ agreement and coordinator reproduction; [record](../results/claims/R26-CUT4-FINITE.md) |
| R26-DIMENSIONS | User-requested correction to prior research note | Full-edge M=BWΨᵀ and support-restricted rank proof, plus constant-field M=BK | INDEPENDENTLY_CHECKED | Dimensions/algebra only under stated field-label assumptions; [record](../results/claims/R26-DIMENSIONS.md) |

For each change, append a new dated record under `results/claims/<ID>.md` (do not overwrite evidence). Coordinator updates this ledger after receiving audit reports.

2026-10-29: workflow 01 completed; [consolidation](../results/CONSOLIDATED.md). No stronger unrestricted lower bound obtained. N1-01 through N1-04, N2-03, and the full bundle N2-04 remain unpromoted. Algebraic reconstruction of selected N2-04 pieces is not independent acceptance of all group/mergeability variants. The user's separate edit to the earlier research note addresses dimensions only, not its other theorem claims.
