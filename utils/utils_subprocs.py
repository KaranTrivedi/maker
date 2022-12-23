#!./venv/bin/python

"""
File for testing subproc command and listing known installed python versions.
"""

import subprocess

print(
    subprocess.check_output(["find /usr/bin/ -maxdepth 1 -regex '/usr/bin/python[0-9]+.[0-9]+'"], shell=True).decode(
        "utf-8"
    )
)