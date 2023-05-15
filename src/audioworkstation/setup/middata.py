#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Create MID file from CSV file."""

from pathlib import Path


from ..libs.sublibs import csv2mid as C2M

CSV_FILENAME = "middata/example.csv"
MID_FILENAME = "mid/example.mid"


def midfile():
    """Create MID file from CSV file.

    :note: "middata/example.csv"
    :note: "mid/example.mid"
    """
    cwd = Path(__file__).parents[1]

    C2M.generate(csvfile=f"{cwd}/CSV_FILENAME", midifile=MID_FILENAME)


if __name__ == "__main__":
    print(__file__)
