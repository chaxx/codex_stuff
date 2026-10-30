# Workflow: verify/strengthen upper bounds

1. `algebraic_sketches` audit the polynomial deletion transform, fixed dimension N=binom(n,2), rank factorization and randomized fingerprint.
2. `upper_bounds` independently derive public/private message complexities, error bounds, finite-field random seed costs and exact certificate construction. Compare to both original and research note.
3. `experiments` devise finite counterexamples to hidden assumptions (k=1, k close n, failures deleting sampled neighbors, tiny field, cyclic graph).
4. `proof_auditor` receive only candidate theorems at first, then full proofs; write specific verdict.
5. `manuscript_editor` produce revised theorem/lemma LaTeX and correction log only for checked assertions.

Record output type (decision/partition/certificate), polynomial-time vs exponential-time decoder, and randomness explicitly.
