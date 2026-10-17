#!/usr/bin/env python3
"""Install optional alignment dependencies into this skill's isolated venv."""
import subprocess,sys,venv
from pathlib import Path
root=Path(__file__).resolve().parents[1]
env=root/'.venv'
if not (env/'bin/python').is_file():venv.EnvBuilder(with_pip=True).create(env)
subprocess.run([str(env/'bin/python'),'-m','pip','install','-r',str(root/'scripts/requirements.txt')],check=True)
subprocess.run([str(env/'bin/python'),str(root/'scripts/lesson.py'),'doctor'],check=True)
