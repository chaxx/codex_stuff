# Research protocol for Codex

You are assisting a TCS researcher writing *Annihilator Sketches and the Complexity of Distributed Vertex Connectivity*. The user wants rigorous mathematics and independent, adversarial proof verification. Favor conceptual breakthroughs over superficial restatement.

## Baseline & conventions

1. Read `context/definitions.md`, `context/claims.md`, `context/open-problems.md`, and the selected workflow **before** choosing a proof path.
2. The authoritative input is `sources/draft/paper-body.pdf` / its extracted text. Prior AI notes in `sources/prior-notes/` are **not authoritative**.
3. Communication: each vertex knows exactly its own neighborhood, messages sent simultaneously to a referee; deterministic max bits **per vertex** is the key lower-bound measure. No public shared neighborhood knowledge. Randomized protocols specify public vs private randomness exactly.
4. k-vertex-connected means graph has >k vertices and remains connected after deleting every F with |F|<k (not <=k).
5. Original AGM-style edge universe is fixed [n] choose 2. Contraction changes the number of aggregate rows, **not** the ambient number of edge coordinates. Any proof restriction to support S is an analytic compression, not a different protocol.
6. Never assert that an unproved result follows merely from small-n computation, informal probabilistic intuition, or inaccessible citation.
7. Distinguish strong certificate / forest recovery / component partitions / boolean decision, and polynomial decoding vs exponential postprocessing.

## Coordination

For nontrivial new research, delegate **independent** threads to named `.codex/agents` roles, such as `lower_bounds`, `upper_bounds`, `algebraic_sketches`, `literature`, `experiments`. A fresh `proof_auditor` MUST review the best candidate, and must not receive the proposing agent's scratch reasoning until after an independent attack. Use `manuscript_editor` only after claim audit. If no subagent tools are exposed, say so and run these stages sequentially with explicitly separated notes, rather than pretending independent review occurred.

Subagents should normally write only `results/agents/<role>/...` (or scripts under `verification/new/` assigned to them); only the coordinator updates `context/claims.md`, `context/issues.md`, and `results/CONSOLIDATED.md`. Share file ownership before parallel work. Avoid concurrent edits to shared files.

For each new theorem report:
- Statement with exact n, k range, randomness, communication definition, runtime/output and success probability.
- Full proof with named technical lemmas and precise source dependencies.
- Adversarial counterexample search (small cases, extreme k, zero weights, field characteristic, signs, rank, conditioned dependence).
- Independent verdict with either a complete proof or exact first invalid inference and a concrete test.
- Claim status in ledger, and bibliographic check. Never label a claim 'verified' solely because a theorem sounds familiar.

## Reports

End each research run with `results/CONSOLIDATED.md` listing **proved**, **candidate/conditional**, **refuted**, **open**, and **next steps**, with precise file pointers and links/references. Put polished LaTeX in `manuscript/` only when mathematical content has been checked; compile it and log the result. Prefer definitions → main proof → technical lemmas, without meta-commentary interleaved in formal proofs.

## Hard prohibitions

Do not overwrite `sources/`. Do not treat PDF text extraction artifacts as original source. No invented citation, theorem numbering, or algorithmic bounds. Do not quietly weaken/strengthen a theorem. Do not use an agent's positive self-review as independent verification. Avoid unbounded external API or running expensive experiments without user approval.
