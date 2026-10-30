# Aborted audit: inherited proof context

This first auditor instance was spawned with the complete coordinator history.
That history already contained tool outputs printing the original draft's
Section 6 proof and the prior note's cut-space and bounded-rank proofs.
Consequently this instance cannot satisfy the workflow's requirement for an
initial attack without the proposing proof.

The auditor immediately informed the coordinator and requested a replacement
with `fork_turns="none"`. No mathematical verdict from this instance is offered
or should count as independent verification. The replacement should receive
only isolated statements and source definitions until its initial findings
have been saved.
