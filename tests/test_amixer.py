#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import unittest

# test amixer
from src.audioworkstation.libs.audio import amixer as Master


class TestMaster(unittest.TestCase):

    def test_volume(self) -> None:
        print(Master.volume())


if __name__ == '__main__':
    unittest.main()
