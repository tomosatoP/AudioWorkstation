#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from json import dump


def screens():
    settings = dict()
    fs_settings = "config/fluidsynth.json"
    sfonts = ["sf2/FluidR3_GM.sf2"]

    settings["keyboard"] = {"settings": fs_settings, "soundfont": sfonts}
    settings["metronome"] = {"settings": fs_settings, "soundfont": sfonts}
    settings["player"] = {"settings": fs_settings, "soundfont": sfonts}

    with open("config/screen.json", "wt") as fw:
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

    with open("config/gmsoundsetgroping.json", "wt") as fw:
        dump(grouping, fw, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    print(__file__)
