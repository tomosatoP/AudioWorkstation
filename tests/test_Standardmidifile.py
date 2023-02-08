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

    def test_title(self) -> None:
        self.assertEqual(self.midifile.title(), 'usseiwa')


if __name__ == '__main__':
    unittest.main()
