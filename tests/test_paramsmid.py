#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""unittest libs/sublibs/paramsmid.py and libs/sublibs/csv2mid.py"""

import unittest
from pathlib import Path

from audioworkstation.libs.sublibs import paramsmid as PMID
from audioworkstation.libs.sublibs import csv2mid as C2M


CSV_FILENAME = "example/example.csv"
MID_FILENAME = "mid/example.mid"


class TestSMF(unittest.TestCase):
    def setUp(self) -> None:
        C2M.generate(csvfile=CSV_FILENAME, midifile=MID_FILENAME)

        fo = Path(MID_FILENAME)
        self.midifile = PMID.StandardMidiFile(fo)
        return super().setUp()

    def test_channels_preset(self) -> None:
        self.assertEqual(self.midifile.channels_preset()[0], 0)

    def test_title(self) -> None:
        self.assertEqual(self.midifile.title(), "example title")

    def test_instruments(self) -> None:
        self.assertEqual(self.midifile.instruments(), ["Piano", "Piano"])

    def test_lyrics(self) -> None:
        self.assertEqual(self.midifile.lyrics(), ["example lyric"])

    def test_total_tick(self) -> None:
        self.assertEqual(self.midifile.total_tick(), 3840)


if __name__ == "__main__":
    unittest.main()
