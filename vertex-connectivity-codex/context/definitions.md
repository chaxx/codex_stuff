# Shared problem definitions (working)

- G=(V,E) undirected simple labeled graph, V=[n]. Each of n players v knows **only** N_G(v), sends one simultaneous message to a referee; no interaction.
- `B` denotes worst-case **maximum number of bits sent by one vertex**, not nB total. Encoders may be arbitrary and vertex-specific unless explicit restriction stated. Deterministic models have no random inputs.
- Connectivity (k=1) asks whether G connected.
- k-vertex-connected for 1<=k<n: G has more than k vertices and G-F is connected for all F⊆V with |F|<k. Distinguish k-connected versus disconnected promise when needed.
- `N=binom(n,2)` is **fixed ambient edge universe**, including nonexistent edges. Signed incidence row vectors live in F_Q^N. Contracting components changes row count, not N. For F, polynomial P_F(X)=∏_{z∈F}(X-a_z) zeroes failed endpoints; aggregate row sketches cancel internal edges. Analytic restriction to S⊆edge-universe permitted only when explicitly labeled.
- Strong certificate H⊆G satisfies CC(H-F)=CC(G-F) for every |F|<k. Boolean decision is strictly weaker as output requirement.
- Separate: public vs private randomness; worst-case vs expected communication; w.h.p. over public/private coins; polynomial vs all-F enumeration.
- Distinguish: arbitrary encoder, additive linear sketch, common-map sketch, exactly XOR-mergeable, OR-union-mergeable, monotone-bit restriction.

## Fixed-edge rank factorization (clarified 2026-10-29)

For r components of a known spanning subgraph of G−F, let R be their r×(n−|F|) row-aggregation matrix and let the surviving incidence matrix be (n−|F|)×N, retaining every original potential-edge column. Their product B is r×N. The transformed deterministic rank certificate is

\[
M=BW\Psi^{\mathsf T},\qquad
B:r\times N,\quad W:N\times N,\quad\Psi:t\times N,\quad M:r\times t.
\]

Here W is diagonal with W_{uv,uv}=P_F(a_u)P_F(a_v), and Ψ_{j,uv}=(a_u a_v)^j. Failed-endpoint coordinates have zero weights; full W need not be invertible. Restriction to active inter-component edge support S is an analytic step, with B_S:r×|S|, W_S:|S|×|S|, Ψ_S:t×|S|. Only W_S is inverted. Contraction changes aggregate rows, not N or original edge identities.

The draft's raw neighbor-sketch Vandermonde matrix is vertex-indexed and has n columns; it is a different map from this transformed edge-indexed Ψ. With all draft coordinates retained, t=2d+k−|F|+1. See the user-requested correction in `sources/prior-notes/vertex_connectivity_research_note.tex` and its scoped dimension audit in `results/agents/proof_auditor/2026-10-29-dimensions.md`.
