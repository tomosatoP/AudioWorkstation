#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from math import pow, log10


_min_gain: float = 10**-3  # 10**-4
_ratio: float = 25  # 20


def gain2dB(value: float) -> int:
    if value < _min_gain:
        value = _min_gain
    return int(_ratio * log10(value / _min_gain))


def dB2gain(value: int) -> float:
    return _min_gain * pow(10.0, float(value) / _ratio)


if __name__ == "__main__":
    print(__file__)
