# R26-CUT4-FINITE

## 2026-10-29 — COMPUTATION_CHECKED

The full universe of 128⁴=268,435,456 complement-normalized tuples of Boolean local truth tables on K₄ has no cut recognizer. Arbitrary nonlinear vertex-specific encoders and arbitrary referee are included, but each local alphabet has exactly at most two symbols. Exact bitset search covers 448 cut/noncut separation constraints with sound prefix pruning; 499,841 nodes. Python and C++ agree; the coordinator inspected the method and reran Python, obtaining identical counts. [Report](../agents/experiments/2026-10-29-report.md), [recorded results](../../verification/new/run_20261029_checks.json), [reproduction](../COORDINATOR-RECHECK-2026-10-29.json).

Balanced edge ownership gives two fixed bits per vertex, so the precise finite fixed-length cost is two. This is finite computational verification, not a formally machine-checked theorem or asymptotic bound. It does not include a three-symbol alphabet represented by empty/0/1 at variable maximum length one. The separate m=5 anchored HiGHS infeasibility has no certificate and is not included in this claim.
