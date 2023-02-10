#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import unittest

# test class standardmidifile
from src.audioworkstation.libs.items import standardmidifile as SMF
from pathlib import Path


class TestSMF(unittest.TestCase):

    def setUp(self) -> None:
        midifilename = 'mid/R01698G2.mid'
        # title='usseiwa'
        fo = Path(midifilename)
        self.midifile = SMF.StandardMidiFile(fo)
        return super().setUp()

    def test_channels_preset(self) -> None:
        self.assertEqual(self.midifile.channels_preset()[0], 22)

    def test_title(self) -> None:
        self.assertEqual(self.midifile.title(), 'usseiwa')

    def test_instruments(self) -> None:
        self.assertEqual(self.midifile.instruments(), [])

    def test_lyrics(self) -> None:
        self.assertEqual(self.midifile.lyrics(), [])

    def test_total_tick(self) -> None:
        self.assertEqual(self.midifile.total_tick(), 295600)


if __name__ == '__main__':
    unittest.main()
