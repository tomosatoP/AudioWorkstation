#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Compile Cython files."""

from pathlib import Path
from subprocess import run


def purepython() -> bool:
    """purepython _summary_

    :return bool: _description_
    """

    print("cythonize -i3 'paramsmid.py'...")

    cwd = Path(__file__).parents[1]
    py_filename: str = f"{cwd}/libs/sublibs/paramsmid.py"
    command: str = f"cythonize -i3 {py_filename}"

    res = run(args=command.split())

    return True if not res.returncode else False


if __name__ == "__main__":
    print(__file__)
