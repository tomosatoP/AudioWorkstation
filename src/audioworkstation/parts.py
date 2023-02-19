#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from math import pow, log10

_min_gain = 10**-4


def _gain2dB(value: float) -> int:
    if value < _min_gain:
        value = _min_gain
    return int(20 * log10(value / _min_gain))


def _dB2gain(value: int) -> float:
    return _min_gain * pow(10.0, float(value) / 20.0)


if __name__ == "__main__":
    print(__file__)
