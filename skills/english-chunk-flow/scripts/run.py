#!/usr/bin/env python3
"""Select this skill's optional runtime without modifying system Python."""
import os,sys
from pathlib import Path
root=Path(__file__).resolve().parents[1]
python=root/'.venv/bin/python'
if not python.is_file():python=Path(sys.executable)
os.execv(str(python),[str(python),str(root/'scripts/lesson.py'),*sys.argv[1:]])
