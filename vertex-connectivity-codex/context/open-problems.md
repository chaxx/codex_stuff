# Priority questions and specific proof targets

1. **Main problem: deterministic k=1, arbitrary vertex-neighborhood encoders.** Improve B=Ω(√n), ideally B≥n/polylog n. Do NOT conflate linear-sketch restrictions with general communication. Look for hard graph families with no small reservoir and a nontrivial global consistency argument.
2. **Two-sheeted-lift/cut-space approach.** Find a theorem that arbitrary h_v:S→[2^B] admit a common cut input s and nontrivial symmetric high-rank row perturbation D making all h_v(s+D_v)=h_v(s), or identify a counterexample/strong upper bound. Understand the zero-root-row requirement and quantify m, B.
3. **Alternative hard families.** Cover partitions, graph lifts, tree matroid sensitivity, partition lattice, chromatic polynomial, connectivity Fourier spectrum, topology; attempt one family dissimilar to two cliques.
4. **Obstruction.** Small-rank switches can be separated by O(log n) bits in some vertex-dependent sketch families: avoid using them as universal hard witnesses.
5. **Upper bounds.** Optimize both communication and polynomial-time decoding under strong certificate and decision output types; verify advertised gains in prior notes.
6. **Proof correctness.** Fully audit draft's annihilator sketch including signs, Φ uniformity, F range, private-random sampling coupling, Borůvka progress, and sparse certificate count.
7. **Literature.** Cross-check currently known deterministic SMP connectivity bounds and potential stronger results (post 2025 included) before novelty claims.
