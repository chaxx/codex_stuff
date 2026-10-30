# R26-DIMENSIONS

## 2026-10-29 — INDEPENDENTLY_CHECKED, scoped source correction

The user explicitly requested editing `sources/prior-notes/vertex_connectivity_research_note.tex` to restore the fixed N=binom(n,2) ambient edge coordinates. This supersedes the blanket source-immutability guideline for that specified TeX file only. Original PDFs and author draft remain unchanged.

The edited deterministic rank lemma uses B:r×N, W:N×N, transformed Ψ:t×N, M=BWΨᵀ:r×t. Contraction sums rows; inactive original-edge columns are retained. Only the analytically restricted W_S is inverted. The raw n-column vertex Vandermonde map is distinguished explicitly. Constant-field M=BK has B:r×N,K:N×D,M:r×D. The transform expansion, edge signs, zero-support case, field-label assumptions, and right-inverse argument were reviewed separately: [scoped audit](../agents/proof_auditor/2026-10-29-dimensions.md).

[Edit/build record](../agents/algebraic_sketches/2026-10-29-dimension-correction.md), [corrected PDF](../dimension-correction/vertex_connectivity_research_note.pdf), [patch](../dimension-correction/dimension-correction.patch). Two-pass compilation succeeded with no warnings; four finite consistency cases passed. This record does not certify the prior note's surrounding probability, complexity, or other theorem claims.
