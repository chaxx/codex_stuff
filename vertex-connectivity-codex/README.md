# Distributed Vertex Connectivity — Codex research workspace

**State:** Research project, not a finished or verified paper. Original author draft is `sources/draft/paper-body.pdf`. Prior AI research notes are **candidates**, NOT proof-checked accepted results.

## Start here (Mac / zsh)

1. Unzip the archive and open Terminal in `vertex-connectivity-codex`.
2. Install the Codex CLI if needed, following the official Codex installation documentation; for a Node installation, `npm install -g @openai/codex`.
3. Authenticate with `codex login` (if prompted), and mark this folder trusted when asked (project `.codex` config requires trust).
4. Run `python3 scripts/validate_workspace.py` (checks files and configuration; does **not** run Codex).
5. Run `codex` in this directory. Paste a prompt from `prompts/` or ask:

   > Run the harness in `workflows/01-deterministic-connectivity.md`. Use the custom agents, work in parallel when independent, commission a fresh proof audit, and produce a consolidated report with clearly labeled proved/open/refuted claims.

   Alternatively `./scripts/run_harness.sh lower-bound` submits that workflow to `codex exec` (requires an installed and authenticated Codex CLI). Use `./scripts/run_harness.sh help` for other modes.

This archive is self-contained for *input reference material*: it includes the original PDF, its extracted text, two prior research notes with LaTeX sources, and the prior experimental scripts. It does **not** contain the author's original editable source for `paper-body.pdf`: place that separately in `manuscript/` when ready. Agents must not silently recreate that source and call it the original.

## Compile the drafts

Install a TeX distribution with `pdflatex` and `latexmk` (for example, MacTeX).
From this project root (`vertex-connectivity-codex`), run:

```sh
latexmk
```

The root `.latexmkrc` builds the current lower-bound manuscript and both research
notes. PDFs, logs, and auxiliary files go into `build/`, leaving the reference
PDFs under `sources/` unchanged. The corrected note is compiled from
`sources/prior-notes/vertex_connectivity_research_note.tex`.

To compile only that note, or watch it and rebuild after edits:

```sh
latexmk sources/prior-notes/vertex_connectivity_research_note.tex
latexmk -pvc sources/prior-notes/vertex_connectivity_research_note.tex
```

Stop watch mode with Ctrl+C. Add future standalone drafts to `@default_files` in
`.latexmkrc`, or pass their paths to `latexmk` explicitly. The author's original
paper remains PDF-only until its editable source is supplied.

## Folder map

- `AGENTS.md` — repository instructions consumed by Codex.
- `.codex/config.toml` and `.codex/agents/*.toml` — project-scoped multi-agent roles; no model hardcoded.
- `sources/draft/` — immutable author draft PDF and extracted text.
- `sources/prior-notes/` — prior AI-generated PDFs/TeX; potential errors to audit.
- `context/` — definitions, claim ledger, open problems, correction list, literature tracking.
- `workflows/` — specific research workflows with mandatory independent review.
- `prompts/` — copy-pasteable Codex tasks.
- `results/` — per-claim findings and reviewer reports.
- `manuscript/` — new article source/drafts; do not overwrite originals.
- `verification/` — prior computational experiments, and new checks.
- `scripts/` — validation and launch scripts.

## Review standard

Each substantial theorem or improvement requires (1) precise formal statement (2) independent derivation/audit without relying on the proposing agent's reasoning (3) proof with every quantifier and conditioning explicit (4) numerical/finite sanity checks when appropriate (5) literature check before novelty claims (6) logged status: conjecture / claimed / checked / refuted / accepted by author.

A passing finite test cannot prove a universal theorem. Likewise a PDF that compiles is not proof verification. Keep different agents' artifacts in different folders; the coordinator is the only writer of canonical ledgers. Do not silently rewrite `sources/`.

## Current focus

Primary: find a stronger deterministic vertex-local simultaneous-message lower bound for **ordinary connectivity** than Ω(√n), ideally Ω(n/polylog n), with arbitrary nonlinear vertex encoders. The current draft's reservoir construction does not exceed the sqrt barrier. Study symmetric consistency of collisions, cut-space / two-sheeted lift, and high-rank differences. Also validate both research notes from scratch.

Secondary: verify annihilator / vertex-filterable sketch transformations and fixed edge-space dimensions; improve random and private-coin upper bounds; proof-check all draft TODOs; produce revised LaTeX with traceable changes.

## Source docs

- Codex custom agents: https://learn.chatgpt.com/docs/agent-configuration/subagents
- Project config: https://learn.chatgpt.com/docs/config-file/config-basic
- Agents API (optional external orchestration): https://developers.openai.com/api/docs/guides/agents-api/multi-agent

Custom `.codex/agents` roles and multi-agent concurrency are based on Codex documentation checked October 2026. They require a compatible Codex client. Independent review is **a required workflow** but never a guarantee of correctness.
