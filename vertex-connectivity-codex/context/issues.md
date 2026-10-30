# Draft/past-note correctness watchlist — unverified status until proof audit

- Original public/private decoder appears to enumerate |F|≤k while k-connected means |F|<k. See original §5 versus §6. Confirm and repair.
- Sign discrepancy: signed adjacency sketch's `sgn(u-v)` and lemma's `sgn(v-u)` must be reconciled; inspect actual matrix orientation.
- Alternate fully random Φ fingerprint uses entries from F_Q\\{0} but argues linear projections are uniform/independent. This is not generally true. Consider drawing from full field; independently check other consequences.
- Clarify that `W` is N×N and edge Vandermonde `Ψ` is t×N, N=binom(n,2); smaller matrices indexed by actual cross-supernode edge support are **proof-only restrictions**. For sketch matrix M rows indexed by r supernodes: M=r×t.
- Validate prime products remain distinct modulo Q; choosing Q=Θ(n³) needs rigorous upper bound on (largest two chosen primes)^2 and explicit prime range.
- Check claimed sparse strong certificate: unstructured union over all deletion-set spanning forests need not have O(kn) edges.
- Verify random-round progress (small k constants) and conditioning, private-random sample coupling, distinction boundary in H-F vs G-F.
- Verify exact claimed deterministic lower bound in abstract versus §6 (Ω(k+√n) vs Ω(min{√n,n/k})).
- Prior note claims may be false or have hidden quantifier gaps. Do not treat them as accepted.

## 2026-10-29 workflow 01 observations

- **Confirmed source discrepancy, not a refutation of the stronger theorem:** the original PDF abstract (physical page 1, lines 19–22) states Ω(k+√n) for 1≤k≤n/6, while §6 Theorem 4 (physical page 13, printed page 12) states Ω(n/(√n+k)). Both formulas were checked visually against the PDF, not inferred from extraction artifacts. This run audits only k=1; the stronger all-k assertion still needs a separate argument.
- **Message framing correction:** concatenating two raw variable-length binary strings is not automatically a decodable 2B-bit simulation. The two-lift reduction has an exact factor 2 for fixed-length/log-alphabet cost. For maximum string length B, encode each symbol in B+1 fixed bits and use 2(B+1). Corrected in the new algebraic report; immutable prior notes were not changed.
- **Audit provenance:** the first auditor inherited parent context containing proofs and aborted before issuing a verdict. A replacement was launched with no inherited history, using isolated statements followed by a separate proof-release stage. The aborted note is preserved in `results/agents/proof_auditor/2026-10-29-aborted-inherited-context.md`.
- **User-requested dimension correction:** the user separately authorized editing `sources/prior-notes/vertex_connectivity_research_note.tex`. Its rank lemma now uses full N-column incidence/measurement matrices and N×N W, with explicit support-only restrictions for the equality proof. The raw vertex-indexed Vandermonde map is distinguished from the transformed edge map. The note uses ε(v,u)=sgn(u−v) consistently with the draft's raw sketch; this does not repair or certify the original draft's separate sign discrepancy. A separate reviewer checked the changed matrix algebra. Compilation outputs and a before/after patch are under `results/dimension-correction/`; other claims in that prior note retain their previous audit status.
