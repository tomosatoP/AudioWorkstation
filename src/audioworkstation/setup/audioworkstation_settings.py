#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from json import dump


def keyboard():
    settings = dict()

    settings["settings"] = "config/fluidsynth.json"
    settings["soundfont"] = [
        "sf2/FluidR3_GM.sf2",
        "sf2/SGM-V2.01.sf2",
        "sf2/YDP-GrandPiano-20160804.sf2",
    ]

    with open("config/keyboard.json", "w") as fw:
        dump(settings, fw, indent=4)


def metronome():
    settings = dict()

    settings["settings"] = "config/fluidsynth.json"

    with open("config/metronome.json", "w") as fw:
        dump(settings, fw, indent=4)


def player():
    settings = dict()

    settings["settings"] = "config/fluidsynth.json"
    settings["soundfont"] = [
        "sf2/FluidR3_GM.sf2",
        "sf2/SGM-V2.01.sf2",
        "sf2/YDP-GrandPiano-20160804.sf2",
    ]

    with open("config/player.json", "w") as fw:
        dump(settings, fw, indent=4)


def gmsounset():
    grouping = dict()

    grouping["ピアノ"] = {"Start": 0, "End": 7}
    grouping["クロマチック・パーカッション"] = {"Start": 8, "End": 15}
    grouping["オルガン"] = {"Start": 16, "End": 23}
    grouping["ギター"] = {"Start": 24, "End": 31}
    grouping["ベース"] = {"Start": 32, "End": 39}
    grouping["ストリングス"] = {"Start": 40, "End": 47}
    grouping["アンサンブル"] = {"Start": 48, "End": 55}
    grouping["ブラス"] = {"Start": 56, "End": 63}
    grouping["リード"] = {"Start": 64, "End": 71}
    grouping["パイプ"] = {"Start": 72, "End": 79}
    grouping["シンセ・リード"] = {"Start": 80, "End": 87}
    grouping["シンセ・パッド"] = {"Start": 88, "End": 95}
    grouping["シンセ・エフェクト"] = {"Start": 96, "End": 103}
    grouping["エスニック"] = {"Start": 104, "End": 111}
    grouping["パーカッシブ"] = {"Start": 112, "End": 119}
    grouping["サウンド・エフェクト"] = {"Start": 120, "End": 127}

    with open("config/gmsoundsetgroping.json", "w") as fw:
        dump(grouping, fw, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    print(__file__)
