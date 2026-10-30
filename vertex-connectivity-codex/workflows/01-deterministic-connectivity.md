# Workflow: improve unrestricted deterministic connectivity lower bound

**Goal:** improve Ω(√n) maximum bits per vertex at k=1, ideally Ω(n/polylog n); arbitrary nonlinear, vertex-specific message functions and arbitrary referee. Not sufficient to improve bounds for linear sketches only.

Parallel first stage: 
1. `lower_bounds`: construct a new hard graph family beyond two cliques and reservoir; attempt fully explicit transcript collision; quantify parameters.
2. `algebraic_sketches`: independently study cut space and 2-lifts, high-rank symmetric collision; test whether linear or group-valued techniques extend to nonlinear functions.
3. `literature`: confirm current benchmark and existing known related lower bounds; distinguish two-party edge partitions from vertex-local one-round model.
4. `experiments`: search small m for collision counterexamples or witnesses via brute force/SAT/MILP when feasible; log search universe precisely.

Second stage: select strongest formal statement; hand to `proof_auditor` **without initial proponent proof**. Auditor attempts adversarial refutation. Only then give proponent proof to audit. If invalid, identify exact first gap, preserving useful lemmas.

Final deliverables: `results/CONSOLIDATED.md` with proofs and limitations; `results/agents/*` independent analyses; `manuscript/lower_bound_candidate.tex` only for fully vetted results. A negative finding is acceptable if clearly reasoned. 
