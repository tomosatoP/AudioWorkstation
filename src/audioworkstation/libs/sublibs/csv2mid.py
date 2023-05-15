#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate a MID(Standard MIDI File) file from a CSV file.

Format of CSV file

    <Format> = <Track Name>, <Bar Number>, <Tick Number>, <Event List>,
    <Value List>

    1. Track Name
        Track Name.

        - example: "Sequencer"
        - example: "Main Melody"
        - example: "Sub Melody"

    2. Bar Number
        Indicates the order of appearance of the measures.

        - example: 0
        - example: 1

    3. Tick Number
        Indicates the timing of event occurrence within a bar in terms of Tick
        conversion. However, the length of a quarter note is 480 ticks.

        - example: 0
        - example: 480
        - example: 960

    4. Event List
        Event.

        - example: "Meta Event","Set Tempo"
        - example: "Midi Event","Note On"
        - example: "Midi Event","Control Change","Channel Volume"

    5. Value List
        Event Value.

        - example: 500000
        - example: 0,69,0x40,200
        - example: 0,0x60

restrictions
    #. Only "GM System Level 1".
    #. Tempo changes and odd time signatures are not supported.
    #. The division is fixed at 480.
"""

from dataclasses import InitVar, dataclass, field
from typing import ClassVar
from re import match
import logging as LSMF
import struct
import csv


# Logger
logger = LSMF.getLogger(__name__)
logger.setLevel(LSMF.DEBUG)
_logger_formatter = LSMF.Formatter("%(asctime)s %(levelname)s %(message)s")
# Logger StreamHandler
_logger_sh = LSMF.StreamHandler()
_logger_sh.setFormatter(_logger_formatter)
logger.addHandler(_logger_sh)


class SmfError(Exception):
    """Exceptions sent out from errcheck func."""

    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        logger.error(f"SMF: {args}")


@dataclass
class HeaderChunk:
    """HeaderChunk is a class that generates "Header chunks"."""

    #: int: "format" specifies the overall organisation of the file.
    format: int = 1
    #: int: "ntrks" is the number of track chunks in the file.
    ntrks: int = 1
    #: int: "division" specifies the meaning of the delta-times. ticks per quarter-note.
    division: int = 480

    def __post_init__(self):
        _SmfEvent.set_division(self.division)

    def __bytes__(self) -> bytes:
        byte_datas: bytes = b"MThd"
        byte_datas += (6).to_bytes(4, "big")
        byte_datas += self.format.to_bytes(2, "big")
        byte_datas += self.ntrks.to_bytes(2, "big")
        byte_datas += self.division.to_bytes(2, "big")

        return byte_datas


@dataclass
class _SmfEvent:
    """_SmfEvent is the base class for event."""

    #: str: "track" is a name that identifies a track.
    track: str

    #: InitVar[str]: bar number
    bar: InitVar[str] = "0"
    #: InitVar[str]: tick count in bar
    tick: InitVar[str] = "0"

    #: ClassVar[int]: division, ticks per quarter-note.
    division: ClassVar[int] = 480
    #: ClassVar[int]: beat
    beat: ClassVar[int] = 4
    #: ClassVar[int]: power of two, 2 represents a quarter-note, etc.
    powers: ClassVar[int] = 2

    event_time: int = field(default=0, init=False)
    delta_time: int = field(default=0, init=False)

    def set_delta_time(self, before_event_time: int) -> None:
        """set_delta_time _summary_

        :param int before_event_time: _description_
        """
        self.delta_time = self.event_time - before_event_time

    @classmethod
    def set_division(cls, division: int):
        cls.division = division

    @classmethod
    def set_rhythm(cls, beat: int, powers: int):
        cls.beat = beat
        cls.powers = powers

    def __post_init__(self, bar, tick) -> None:
        self.event_time = int(bar) * self.beat * self.division * 4 / (2**self.powers)
        self.event_time += int(tick)
        self.event_time = int(self.event_time)

    def __bytes__(self):
        return _convert_to_variable_length_quantity(self.delta_time)

    def __eq__(self, other) -> bool:
        """compare time: equal"""

        if isinstance(other, _SmfEvent):
            return self.event_time == other.event_time
        else:
            name: str = other.__class__.__name__
            message: str = f"comparison between event and {name} is not supported"
            raise SmfError(message)

    def __lt__(self, other) -> bool:
        """compare time: less than"""

        if isinstance(other, _SmfEvent):
            return self.event_time < other.event_time
        else:
            name: str = other.__class__.__name__
            message: str = f"comparison between event and {name} is not supported"
            raise SmfError(message)

    @classmethod
    def name(cls) -> list[str]:
        return []


@dataclass
class _MetaEvnet(_SmfEvent):
    """_MetaEvent is the base class of "Meta Event"."""

    def __bytes__(self):
        return super().__bytes__() + b"\xFF"

    @classmethod
    def name(cls) -> list[str]:
        return super().name() + ["Meta Event"]


@dataclass
class TextEvent(_MetaEvnet):
    """TextEvent is class."""

    #: str: text event
    text: str = ""

    def __bytes__(self):
        byte_datas = b"\x01"
        byte_datas += int(len(self.text)).to_bytes(1, "big")
        byte_datas += bytearray(self.text, encoding="ascii")
        return super().__bytes__() + byte_datas

    @classmethod
    def name(cls) -> list[str]:
        return super().name() + ["Text Event"]


@dataclass
class CopyrightNotice(_MetaEvnet):
    """CopyrightNotice is class."""

    #: str: Copyright Notice
    text: str = ""

    def __bytes__(self):
        byte_datas = b"\x02"
        byte_datas += int(len(self.text)).to_bytes(1, "big")
        byte_datas += bytearray(self.text, encoding="ascii")
        return super().__bytes__() + byte_datas

    @classmethod
    def name(cls) -> list[str]:
        return super().name() + ["Copyright Notice"]


@dataclass
class SequencerTrackName(_MetaEvnet):
    """SequenceTrackName is class."""

    #: str: Sequencer / Track Name
    text: str = ""

    def __bytes__(self):
        byte_datas = b"\x03"
        byte_datas += int(len(self.text)).to_bytes(1, "big")
        byte_datas += bytearray(self.text, encoding="ascii")
        return super().__bytes__() + byte_datas

    @classmethod
    def name(cls) -> list[str]:
        return super().name() + ["SequencerTrack Name"]


@dataclass
class InstrumentName(_MetaEvnet):
    """InstrumentName is class."""

    #: str: Instrument Name
    text: str = ""

    def __bytes__(self):
        byte_datas = b"\x04"
        byte_datas += int(len(self.text)).to_bytes(1, "big")
        byte_datas += bytearray(self.text, encoding="ascii")
        return super().__bytes__() + byte_datas

    @classmethod
    def name(cls):
        return super().name() + ["Instrument Name"]


@dataclass
class Lyric(_MetaEvnet):
    """Lyric is class."""

    #: str: Lyric
    text: str = ""

    def __bytes__(self):
        byte_datas = b"\x05"
        byte_datas += int(len(self.text)).to_bytes(1, "big")
        byte_datas += bytearray(self.text, encoding="ascii")
        return super().__bytes__() + byte_datas

    @classmethod
    def name(cls) -> list[str]:
        return super().name() + ["Lyric"]


@dataclass
class EndOfTrack(_MetaEvnet):
    """end of track"""

    def __bytes__(self):
        return super().__bytes__() + b"\x2F\x00"

    @classmethod
    def name(cls) -> list[str]:
        return super().name() + ["End Of Track"]


@dataclass
class SetTempo(_MetaEvnet):
    """Quarter note microsecond unit time."""

    #: str: Quarter note microsecond unit time
    value: str = "500000"

    def __bytes__(self):
        byte_datas = b"\x51"
        byte_datas += b"\x03"
        byte_datas += int(self.value).to_bytes(3, "big")
        return super().__bytes__() + byte_datas

    @classmethod
    def name(cls) -> list[str]:
        return super().name() + ["Set Tempo"]


@dataclass
class TimeSignature(_MetaEvnet):
    """TimeSignature is expressed as four numbers."""

    #: str: rhythm beat
    nn: str = "4"
    #: str: power to two, rhythm notevalue
    dd: str = "2"
    #: str:
    cc: str = "24"
    #: str:
    bb: str = "8"

    def __post_init__(self, bar, tick) -> None:
        _SmfEvent.set_rhythm(int(self.nn), int(self.dd))
        return super().__post_init__(bar, tick)

    def __bytes__(self):
        byte_datas = b"\x58"
        byte_datas += b"\x04"
        byte_datas += int(self.nn).to_bytes(1, "big")
        byte_datas += int(self.dd).to_bytes(1, "big")
        byte_datas += int(self.cc).to_bytes(1, "big")
        byte_datas += int(self.bb).to_bytes(1, "big")
        return super().__bytes__() + byte_datas

    @classmethod
    def name(cls) -> list[str]:
        return super().name() + ["Time Signature"]


@dataclass
class KeySignature(_MetaEvnet):
    """KeySignature is expressed as four numbers."""

    #: str: 0 is C, +1 ~ +7 is #, -1 ~ -7 is b
    sf: str = "0"
    #: str: 0 is major, 1 is minor
    mi: str = "0"

    def __bytes__(self):
        byte_datas = b"\x59"
        byte_datas += b"\x02"
        byte_datas += int(self.sf).to_bytes(1, "big", signed=True)
        byte_datas += int(self.mi).to_bytes(1, "big")
        return super().__bytes__() + byte_datas

    @classmethod
    def name(cls) -> list[str]:
        return super().name() + ["Key Signature"]


@dataclass
class _SystemExclusiveEvent(_SmfEvent):
    """_SystemExclusiveEvent is the base class of "Sysex Event"."""

    def __bytes__(self):
        return super().__bytes__() + b"\xF0"

    @classmethod
    def name(cls) -> list[str]:
        return super().name() + ["Sysex Event"]


@dataclass
class GmSystemOn(_SystemExclusiveEvent):
    """GM System Level 1."""

    def __bytes__(self):
        return super().__bytes__() + b"\x05\x7E\x7F\x09\x01\xF7"

    @classmethod
    def name(cls) -> list[str]:
        return super().name() + ["GM System On"]


@dataclass
class _MidiEvent(_SmfEvent):
    """_MidiEvent is the base class of "Midi Event"."""

    def __bytes__(self):
        return super().__bytes__()

    @classmethod
    def name(cls) -> list[str]:
        return super().name() + ["Midi Event"]


@dataclass
class NoteOn(_MidiEvent):
    """NoteOn is "Note On"."""

    #: str: channel
    n: str = "0"
    #: str: key number
    kk: str = "60"
    #: str: velocity
    vv: str = "0x40"
    #: str: duration
    dr: str = "100"

    def __bytes__(self):
        byte_datas = (0x90 + int(self.n, 0)).to_bytes(1, "big")
        byte_datas += int(self.kk, 0).to_bytes(1, "big")
        byte_datas += int(self.vv, 0).to_bytes(1, "big")
        return super().__bytes__() + byte_datas

    @classmethod
    def name(cls) -> list[str]:
        return super().name() + ["Note On"]


@dataclass
class NoteOffAfterOn(_MidiEvent):
    """NoteOffAfterOn is "Note off"."""

    #: str: channel
    n: str = "0"
    #: str: key number
    kk: str = "60"
    #: str: velocity
    vv: str = "0x20"

    def __bytes__(self):
        byte_datas = (0x80 + int(self.n, 0)).to_bytes(1, "big")
        byte_datas += int(self.kk, 0).to_bytes(1, "big")
        byte_datas += int(self.vv, 0).to_bytes(1, "big")
        return super().__bytes__() + byte_datas

    @classmethod
    def name(cls) -> list[str]:
        return super().name() + ["Note Off"]


@dataclass
class _ControlChange(_MidiEvent):
    """_ControlChange is the base class of "Midi Event - Control Change"."""

    #: str: channel
    n: str = "0"

    def __bytes__(self):
        byte_datas = (0xB0 + int(self.n, 0)).to_bytes(1, "big")
        return super().__bytes__() + byte_datas

    @classmethod
    def name(cls) -> list[str]:
        return super().name() + ["Control Change"]


@dataclass
class ModulationWheel(_ControlChange):
    """ModulationWeel is "Modulation Wheel"."""

    #: str: value
    vv: str = "0"

    def __bytes__(self):
        byte_datas = (0x01).to_bytes(1, "big")
        byte_datas += int(self.vv, 0).to_bytes(1, "big")
        return super().__bytes__() + byte_datas

    @classmethod
    def name(cls) -> list[str]:
        return super().name() + ["Modulation Wheel"]


@dataclass
class ChannelVolume(_ControlChange):
    """ChannelVolume is "Channel Volume"."""

    #: str: value
    vv: str = "0x70"

    def __bytes__(self):
        byte_datas = (0x07).to_bytes(1, "big")
        byte_datas += int(self.vv, 0).to_bytes(1, "big")
        return super().__bytes__() + byte_datas

    @classmethod
    def name(cls) -> list[str]:
        return super().name() + ["Channel Volume"]


@dataclass
class Pan(_ControlChange):
    """Pan is "Pan"."""

    #: str:
    vv: str = "0x40"

    def __bytes__(self):
        byte_datas = (0x0A).to_bytes(1, "big")
        byte_datas += int(self.vv, 0).to_bytes(1, "big")
        return super().__bytes__() + byte_datas

    @classmethod
    def name(cls) -> list[str]:
        return super().name() + ["Pan"]


@dataclass
class Expression(_ControlChange):
    """Expresson is "Expression"."""

    #: str: value
    vv: str = "0x70"

    def __bytes__(self):
        byte_datas = (0x0B).to_bytes(1, "big")
        byte_datas += int(self.vv, 0).to_bytes(1, "big")
        return super().__bytes__() + byte_datas

    @classmethod
    def name(cls) -> list[str]:
        return super().name() + ["Expression"]


@dataclass
class SustainOn(_ControlChange):
    """SustaionOn is ***."""

    def __bytes__(self):
        byte_datas = (0x40).to_bytes(1, "big")
        byte_datas += (0x40).to_bytes(1, "big")
        return super().__bytes__() + byte_datas

    @classmethod
    def name(cls) -> list[str]:
        return super().name() + ["Sustain On"]


@dataclass
class SustainOff(_ControlChange):
    """SustaionOff is ***."""

    def __bytes__(self):
        byte_datas = (0x40).to_bytes(1, "big")
        byte_datas += (0x00).to_bytes(1, "big")
        return super().__bytes__() + byte_datas

    @classmethod
    def name(cls) -> list[str]:
        return super().name() + ["Sustain Off"]


@dataclass
class _ChannelMode(_MidiEvent):
    """_ChannelMode is base class of "Midi Event - Channel Mode"."""

    #: str: channel
    n: str = "0"

    def __bytes__(self):
        byte_datas = (0xB0 + int(self.n, 0)).to_bytes(1, "big")
        return super().__bytes__() + byte_datas

    @classmethod
    def name(cls) -> list[str]:
        return super().name() + ["Channel Mode"]


@dataclass
class ResetAllControllers(_ChannelMode):
    """ResetAllControllers is ***."""

    def __bytes__(self):
        byte_datas = (0x79).to_bytes(1, "big")
        byte_datas += (0x00).to_bytes(1, "big")
        return super().__bytes__() + byte_datas

    @classmethod
    def name(cls) -> list[str]:
        return super().name() + ["Reset All Controllers"]


@dataclass
class AllNotesOff(_ChannelMode):
    """AllNoteOff is "all notes off message"."""

    def __bytes__(self):
        byte_datas = (0x7B).to_bytes(1, "big")
        byte_datas += (0x00).to_bytes(1, "big")
        return super().__bytes__() + byte_datas

    @classmethod
    def name(cls) -> list[str]:
        return super().name() + ["All Notes Off"]


@dataclass
class ProgramChange(_MidiEvent):
    """ProgramChange is ***."""

    #: str: channle
    n: str = "0"
    #: str: preset number
    vv: str = "0"

    def __bytes__(self):
        byte_datas = (0xC0 + int(self.n, 0)).to_bytes(1, "big")
        byte_datas += int(self.vv, 0).to_bytes(1, "big")
        return super().__bytes__() + byte_datas

    @classmethod
    def name(cls) -> list[str]:
        return super().name() + ["Program Change"]


@dataclass
class ChannelPressure(_MidiEvent):
    """ChannelPressure is ***."""

    #: str: channle
    n: str = "0"
    #: int: threshold
    vv: str = "100"

    def __bytes__(self):
        byte_datas = (0xD0 + int(self.n, 0)).to_bytes(1, "big")
        byte_datas += int(self.vv, 0).to_bytes(1, "big")
        return super().__bytes__() + byte_datas

    @classmethod
    def name(cls) -> list[str]:
        return super().name() + ["Channel Pressuire"]


@dataclass
class PitchWheelChange(_MidiEvent):
    """PitchWheelChange is ***."""

    #: str: channel
    n: str = "0"
    #: str: LSB, centre(non-effect) is 0x00
    ll: str = "0"
    #: str: MSB, centre(non-effect) is 0x40
    mm: str = "0x40"

    def __bytes__(self):
        byte_datas = (0xE0 + int(self.n, 0)).to_bytes(1, "big")
        byte_datas += int(self.ll, 0).to_bytes(1, "big")
        byte_datas += int(self.mm, 0).to_bytes(1, "big")
        return super().__bytes__() + byte_datas

    @classmethod
    def name(cls) -> list[str]:
        return super().name() + ["Pitch Wheel Change"]


def _convert_to_variable_length_quantity(n: int) -> bytes:
    """Convert "n(delta time)" to a "variable length quantity".

    :param int n: delta time
    :return: variable length quantity
    """

    def base_decimal(base: int, n: int) -> list[int]:
        """Convert to a base-decimal.

        :param int base: base
        :param int n: taget number
        :return: Converted value stored in list[int]
        """

        if n < base:
            return [n]
        else:
            digit: list = base_decimal(base, n // base)
        return digit + [n % base]

    quantity: list[int] = base_decimal(2**7, n)

    for i in range(len(quantity) - 1):
        quantity[i] = quantity[i] + 0x80
    return bytes(quantity)


def event_classes() -> set:
    """Return a set of event classes.

    :return: event classes
    """

    def sub_classes(cls):
        return set(cls.__subclasses__()).union(
            [s for c in cls.__subclasses__() for s in sub_classes(c)]
        )

    return sub_classes(_SmfEvent)


def event_data(params: list) -> object:
    """Convert CSV data list to event data object.

    :param list params: csv data list
    :return: event data object
    """
    n_name: int
    data_classes: set = event_classes()

    for data_class in data_classes:
        if not match("_", data_class.__name__):
            if set(data_class.name()) <= set(params):
                n_name = len(data_class.name())
                return data_class(
                    params[0], params[1], params[2], *tuple(params[3 + n_name :])
                )

    return None


def generate(csvfile: str, midifile: str) -> None:
    """Generate a MID file from a CSV file.

    :param str csvfile: CSV filename to be converted.
    :param str midifile: MID filename to be created.
    """

    csv_datas: list = []
    with open(file=csvfile, mode="rt") as f:
        for line in csv.reader(f, dialect="unix"):
            csv_datas.append(line)

    track_names: list = list(map(lambda x: x[0], csv_datas))
    track_names = sorted(set(track_names), key=track_names.index)
    header = HeaderChunk(format=1, ntrks=len(track_names), division=480)

    tracks: list = []
    for i in range(len(track_names)):
        tracks.append([])
        for line in csv_datas:
            if line[0] == track_names[i]:
                tracks[i].append(event_data(line))

    for trk in tracks:
        for ev in trk:
            if isinstance(ev, NoteOn):
                note_off = NoteOffAfterOn(track=ev.track, n=ev.n, kk=ev.kk)
                note_off.event_time = ev.event_time + int(ev.dr)
                trk.append(note_off)

        trk.sort()
        trk[0].set_delta_time = trk[0].event_time
        for i in range(1, len(trk)):
            trk[i].set_delta_time(trk[i - 1].event_time)

    with open(file=midifile, mode="wb") as smf:
        smf.write(bytes(header))
        for trk in tracks:
            smf.write(
                struct.pack(
                    ">" "4s" "L", b"MTrk", sum(list(map(len, (map(bytes, trk)))))
                )
            )
            for ev in trk:
                smf.write(bytes(ev))


if __name__ == "__main__":
    print(__file__)
