#!/usr/bin/env python3
"""Create a source-only, reproducible skill archive; exclude runtimes and lessons."""
from pathlib import Path
import zipfile
root=Path(__file__).resolve().parents[1];skill=root/'skills/english-chunk-flow';out=root/'dist/english-chunk-flow.skill.zip';out.parent.mkdir(exist_ok=True)
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(skill.rglob('*')):
  if not p.is_file() or set(p.parts)&{'.venv','__pycache__'} or p.suffix=='.pyc':continue
  info=zipfile.ZipInfo(str(Path('english-chunk-flow')/p.relative_to(skill)),(2026,10,17,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16;z.writestr(info,p.read_bytes())
with zipfile.ZipFile(out) as z:assert z.testzip() is None
print(out)
