#!/usr/bin/env python3
"""Fast offline integrity/configuration check; does not contact Codex."""
from pathlib import Path
import sys
try:
    import tomllib
except ImportError:
    print('Python 3.11+ needed for tomllib'); sys.exit(2)
R=Path(__file__).resolve().parents[1]
req=['AGENTS.md','README.md','.codex/config.toml','sources/draft/paper-body.pdf','sources/draft/paper-body.txt', 'sources/prior-notes/vertex_connectivity_research_note.pdf','sources/prior-notes/deterministic_connectivity_lower_bounds.pdf']
errors=[]
for p in req:
    if not (R/p).is_file():errors.append('Missing '+p)
for p in sorted((R/'.codex/agents').glob('*.toml')):
    try:
        x=tomllib.loads(p.read_text())
        for key in ('name','description','developer_instructions'):
            if not x.get(key):errors.append(f'{p.name}: missing {key}')
    except Exception as e:errors.append(f'{p.name}: malformed TOML: {e}')
if len(list((R/'.codex/agents').glob('*.toml')))<7:errors.append('Fewer than 7 agent files')
try:
    c=tomllib.loads((R/'.codex/config.toml').read_text())
    if c.get('agents',{}).get('enabled') is not True:errors.append('agents.enabled is not true')
except Exception as e:errors.append(str(e))
print('Root:',R)
print('Agents:',len(list((R/'.codex/agents').glob('*.toml'))))
print('Draft size:',(R/'sources/draft/paper-body.pdf').stat().st_size if (R/'sources/draft/paper-body.pdf').exists() else 'missing')
if errors:
    for e in errors:print('ERROR:',e)
    sys.exit(1)
print('OK: all required files and TOML agent definitions found.')
print('NOTE: This does not verify Codex installation, subagent availability, or theorem correctness.')
