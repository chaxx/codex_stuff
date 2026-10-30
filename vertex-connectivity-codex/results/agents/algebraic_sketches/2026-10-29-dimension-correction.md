# Dimension correction to the prior vertex-connectivity note

Date: 2026-10-29.

## Authorized scope

The user explicitly requested this edit to `sources/prior-notes/vertex_connectivity_research_note.tex`, overriding the workspace's blanket immutable-source rule for this one TeX file. The original author draft and existing source PDFs were not changed. This is a dimensional clarification and repair of the rank proof's notation, not a full audit or endorsement of the note's other claims.

Edited file: `sources/prior-notes/vertex_connectivity_research_note.tex`.

Corrected PDF: `results/dimension-correction/vertex_connectivity_research_note.pdf`.

Review artifacts: the original TeX copy `results/dimension-correction/vertex_connectivity_research_note.before.tex` and the unified patch `results/dimension-correction/dimension-correction.patch`.

## Changes and mathematical reason

Section 2 now defines the fixed original edge universe `E=binom([n],2)`, of size `N=binom(n,2)`, before Lemma 2.1. Every original or aggregate incidence row has `N` entries. Contraction adds rows and cancels internal edges; it does not replace original edges by pairs of supernodes, and distinct original edges between the same supernodes retain separate columns.

The primary factorization is explicitly

\[
 M_{r\times t}=B_{r\times N}W_{N\times N}\Psi^T_{N\times t},
 \qquad \Psi\in\mathbb F_Q^{t\times N}.
\]

The proof defines the original surviving-vertex incidence matrix `B_F` as `(n-|F|) x N`, the row aggregation matrix `R` as `r x (n-|F|)`, and `B=R B_F`. The endpoint orientation is `+1` at the smaller label, `-1` at the larger, consistent with the author's displayed raw signed-neighbor sketch.

It also spells out the transformation from the stored moments using the coefficients of `P_F`. The draft's **raw vertex-indexed** Vandermonde map has `n` columns; the **transformed edge-indexed** `Psi` here has `N` columns. These two maps are now expressly distinguished. Retaining all of the draft's transformed moments gives `t=2d+k-|F|+1`, indexed `0,...,t-1`.

The full diagonal `W` has one entry `P_F(a_u)P_F(a_v)` for every potential original edge `{u,v}`. It vanishes on failed-endpoint coordinates, so the full `W` is not asserted to be invertible. Likewise, the full `Psi` need not have column rank `N`.

Only within the equality proof, the active support `S` of surviving intercomponent edges is selected. For `m=|S|`, the analytic restrictions are `B_S: r x m`, `W_S: m x m`, `Psi_S: t x m`. They satisfy the same product `M=B_S W_S Psi_S^T`. When `1<=m<=d`, `W_S` is invertible and `Psi_S` has full column rank, so `W_S Psi_S^T` has a `t x m` right inverse. This preserves the rank of `B_S`. The `m=0` case is handled separately. Thus the original rank theorem survives with the protocol's full ambient dimensions intact.

Section 3's constant-field construction now also records `M: r x D`, `B: r x N`, and its edge-feature matrix `K: N x D`, so `M=BK`. Its random matrix `Phi: m x n` remains vertex-indexed by construction; this does not conflict with the `N`-dimensional incidence space. Dimensions of `Phi_F` and the kernel vectors are explicit.

No other theorem, asymptotic bound, field-size choice, or source-draft content was changed.

## Verification

Two passes of the following command completed successfully:

```sh
pdflatex -interaction=nonstopmode -halt-on-error \
  -output-directory=results/dimension-correction \
  sources/prior-notes/vertex_connectivity_research_note.tex
```

Output: 16-page PDF, 391,161 bytes. The final compilation log has no LaTeX errors, warnings, unresolved references, or overfull boxes. The log is `results/dimension-correction/vertex_connectivity_research_note.log`; both pass outputs are preserved as `pdflatex-pass1.stdout` and `pdflatex-pass2.stdout` in that directory.

A dependency-free finite check compared three independently computed quantities over `F_101`: full-coordinate `B W Psi^T`, support-restricted `B_S W_S Psi_S^T`, and moments transformed directly from the stored vertex sketches. It used five vertices with labels `2,3,5,7,11` and edges `{01,02,12,23,04,14,34}` (zero-based labels). All four cases passed:

| Failed vertices | Aggregate components | N | t | Active original edges | Matrix rank |
|---|---|---:|---:|---:|---:|
| `{4}` | `{0,1}`, `{2,3}` | 10 | 6 | 2 | 1 |
| `{4}` | `{0,1,2,3}` | 10 | 4 | 0 | 0 |
| empty | five singleton components | 10 | 17 | 7 | 4 |
| `{0,1}` | `{2,3,4}` | 10 | 3 | 0 | 0 |

These cases include parallel edges after aggregation, internal edges, absent coordinates, failed-endpoint zero weights, and empty active support. The check verifies the dimensional reformulation on finite examples; it is not the proof of the rank theorem.

The broader existing `rank_checks()` suite was not run: its import requires `networkx`, which is not installed in the base Python environment. No dependency was installed for this source clarification. The successful direct checks above and the written algebra are the validation performed.

## Preservation checks

The two source PDFs have the same SHA-256 before and after this edit:

- `sources/prior-notes/vertex_connectivity_research_note.pdf`: `b9408f3b3f886ba05a80a63d0c7617775d932f7d183e373a9ec2db23b5fd7c95`.
- `sources/draft/paper-body.pdf`: `9e675cac6ca298a20feb79a6b46a5aa11b21ddce363cba524793e89e0aae8e8d`.

The original TeX SHA-256 (also the preserved `.before.tex` copy) is `75d722dccdbf564878b4f29225622558957ae5c6ff68990fdd3ed1128951cddd`.

## Separate harness scope note

The low-rank separator theorem from this research run obstructs universal collision lemmas deduced solely from a message budget for arbitrary local maps. It does not by itself rule out proof strategies that additionally exploit the assumption that those maps correctly decide connectivity. This qualification belongs with the lower-bound harness findings; it was not inserted into this unrelated dimension correction.
