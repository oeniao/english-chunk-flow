#!/usr/bin/env python3
"""Copy this skill into a local discovery directory without overwriting it."""
import argparse,shutil
from pathlib import Path
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--dest',type=Path)
p.add_argument('--host',choices=['generic','claude','grok','workbuddy'],default='generic')
p.add_argument('--project',type=Path,help='Install into this workspace instead of the user home')
a=p.parse_args();source=Path(__file__).resolve().parents[1]/'skills/english-chunk-flow'
if a.dest and a.project:p.error('--dest and --project are mutually exclusive')
if a.host=='workbuddy' and not (a.project or a.dest):p.error('WorkBuddy: use the skill ZIP import UI, or supply --project /workspace for .codebuddy/skills.')
folder={'generic':'.agents','claude':'.claude','grok':'.grok','workbuddy':'.codebuddy'}[a.host]
base=a.project.expanduser().resolve() if a.project else Path.home()
dest=(a.dest.expanduser() if a.dest else base/folder/'skills/english-chunk-flow').resolve()
if dest.exists():p.error('Destination already exists; choose a new --dest or manage the existing installation explicitly.')
dest.parent.mkdir(parents=True,exist_ok=True)
shutil.copytree(source,dest,ignore=shutil.ignore_patterns('.venv','__pycache__','*.pyc'))
print('Installed:',dest)
print('Optional setup: python3',dest/'scripts/setup.py')
print('Ask your host to use English Chunk Flow; Claude Code / Grok Build: /english-chunk-flow. Refresh skill discovery if needed.')
