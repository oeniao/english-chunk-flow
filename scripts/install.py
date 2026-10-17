#!/usr/bin/env python3
"""Copy this skill into a local discovery directory without overwriting it."""
import argparse,shutil
from pathlib import Path
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--dest',type=Path,default=Path.home()/'.agents/skills/english-chunk-flow')
a=p.parse_args();source=Path(__file__).resolve().parents[1]/'skills/english-chunk-flow';dest=a.dest.expanduser().resolve()
if dest.exists():p.error('Destination already exists; choose a new --dest or manage the existing installation explicitly.')
dest.parent.mkdir(parents=True,exist_ok=True)
shutil.copytree(source,dest,ignore=shutil.ignore_patterns('.venv','__pycache__','*.pyc'))
print('Installed:',dest)
print('Optional setup: python3',dest/'scripts/setup.py')
print('Invoke $english-chunk-flow in a new host conversation.')
