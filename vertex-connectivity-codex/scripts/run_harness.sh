#!/usr/bin/env bash
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$here"
case "${1:-help}" in
  lower-bound|upper-bound|audit|paper)
    if ! command -v codex >/dev/null; then
      echo "Codex CLI missing. Install/sign in, then open this directory with codex." >&2
      exit 127
    fi
    prompt="$(cat "prompts/$1.txt")"
    # The project is deliberately NOT run with unsafe sandbox or approval overrides.
    codex exec "$prompt"
    ;;
  help|--help|-h)
    echo "Usage: ./scripts/run_harness.sh {lower-bound|upper-bound|audit|paper}"
    echo "Or run 'codex' interactively in this directory and paste prompts/*.txt"
    ;;
  *) echo "Unknown workflow: $1" >&2; exit 2;;
esac
