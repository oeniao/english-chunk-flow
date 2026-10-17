#!/usr/bin/env python3
"""Check local Markdown links and exclude workstation paths from public sources."""
from pathlib import Path
import re
root=Path(__file__).resolve().parents[1];errors=[]
for p in root.rglob('*'):
 if not p.is_file() or set(p.parts)&{'.git','.venv','__pycache__','output','dist'}:continue
 if p.suffix not in {'.md','.py','.yml','.yaml','.html','.js','.css','.json','.txt'}:continue
 text=p.read_text()
 if re.search(r'/(?:Users|private/var|var/folders)/',text):errors.append(str(p.relative_to(root))+': workstation path')
 if p.suffix!='.md':continue
 for link in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)',text):
  link=link.strip('<>').split('#')[0]
  if not link or re.match(r'[a-z]+:',link):continue
  if not (p.parent/link).exists():errors.append(str(p.relative_to(root))+': missing '+link)
if errors:raise SystemExit('\n'.join(errors))
print('Documentation links and public-source paths verified.')
