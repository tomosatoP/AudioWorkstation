#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Create a configuration file for the application."""

from json import dump
from pathlib import Path
from subprocess import run


def cbuild() -> None:
    command: list[str] = ["cythonize", "-i3", "libs/sublibs/standardmidifile.py"]
    run(args=command)


def screens() -> None:
    """Create configuration files for various child screens.

    :note: "config/screen.json"
    """

    settings = dict()
    fs_settings = "config/fluidsynth.json"
    sfonts = ["sf2/FluidR3_GM.sf2"]

    settings["keyboard"] = {"settings": fs_settings, "soundfont": sfonts}
    settings["metronome"] = {"settings": fs_settings, "soundfont": sfonts}
    settings["player"] = {"settings": fs_settings, "soundfont": sfonts}

    with open("config/screen.json", "wt") as fw:
        dump(settings, fw, indent=4)


def gmsounset() -> None:
    """Create a GM sound set group information file.

    :note: "config/gmsoundsetgroping.json"
    """

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


def desktop() -> None:
    """Register as a desktop application

    :note: "~/.local/share/applications/AudioWorkstation.desktop"
    :note: "~/AudioWorkstation/AudioWorkstation.sh"
    """

    cdir: str = str(Path.cwd())
    hdir: str = str(Path.home())

    command: list[str] = list()
    command.append(". venv/bin/activate")
    command.append("python3 -m audioworkstation")
    command.append("deactivate")
    filename = f"{cdir}/AudioWorkstation.sh"

    with open(file=filename, mode="wt") as f:
        for line in command:
            print(line, file=f)

    Path(filename).chmod(0o755)

    desktop: list[str] = list()
    desktop.append("[Desktop Entry]")
    desktop.append("Name=AudioWorkstation")
    desktop.append("GenericName=MIDI sequencer")
    desktop.append("Comment=Play an instrument with a USB-MIDI keyboard")
    desktop.append(f"Path={cdir}/")
    desktop.append(f"Exec={cdir}/AudioWorkstation.sh")
    desktop.append("Terminal=false")
    desktop.append("Type=Application")
    desktop.append("Icon=multimedia-volume-control-symbolic")
    desktop.append("Categories=Audio;AudioVideo")
    filename = f"{hdir}/.local/share/applications/AudioWorkstation.desktop"

    with open(file=filename, mode="wt") as f:
        for line in desktop:
            print(line, file=f)


if __name__ == "__main__":
    print(__file__)
