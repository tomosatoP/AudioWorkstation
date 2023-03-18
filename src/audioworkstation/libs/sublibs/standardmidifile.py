#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Analyze MIDI files according to  SMF (Standard MIDI File) format.

class StandardMidiFile
 - param
   - pathlib.Path midifile: SMF
 - method
   - str title(): title
   - int total_tick(): total ticks
   - list[str] instruments(): instruments
   - list[str] lyrics(): lyrics
   - list[int] channels_preset(): channels preset

:reference:
    MIDI1.0規格書(日本語版98.1) ISBN4-8456-0348-9 C3055  http://www.amei.or.jp/

        2. MIDI 1.0
        4. スタンダードMIDIファイル1.0
"""
import struct
from typing import Union
from pathlib import Path

FOURCC = ">" "4s"
CKDR = FOURCC + "L"
HEADER_CHUNK = CKDR + "HHH"
BYTE = ">" "B"


class StandardMidiFile:
    """StandardMidiFile.

    :param pathlib.Path midifile:
    """

    def __init__(self, midifile: Path) -> None:
        self._header: list = list()
        self._tracks: list = list()
        self._last_event_type: int = -1

        ckID: bytes
        ckSize: int
        offset: int
        delta_time: int

        current_tick: int
        list_event: list

        self._smf: bytes = midifile.read_bytes()
        self._header, offset = self._header_chunk()

        for _ in range(self._header[3]):
            ckID, ckSize, offset = self._unpack(offset, CKDR)

            current_tick = 0
            list_event = []
            while ckSize:
                ckSize += offset
                delta_time, offset = self._delta_time(offset)
                current_tick += delta_time

                event, offset = self._dequeue_event(offset)
                list_event.append([current_tick, *event])
                ckSize -= offset

            self._tracks += [list_event]

    def channels_preset(self) -> list:
        """Get a list of preset numbers for each of the 16 channels.

        :return list[int]:
        """
        channels: list = [[]] * 16
        for track in self._tracks:
            for event in track:
                if event[1] == 0xC:
                    channels[event[2]] = event[3]
        return channels

    def title(self) -> str:
        """Get Title.

        :return str:
        """
        for event in self._tracks[0]:
            if all([event[1] == 0xFF, event[2] == 0x03]):
                return event[3].decode("sjis")
        return "-"

    def instruments(self) -> list:
        """Get a list of instrument names for each of the 16 channels.

        :return list[str]:
        """
        names: list = list()
        for track in self._tracks:
            for event in track:
                if all([event[1] == 0xFF, event[2] == 0x04]):
                    names += [event[3].decode("sjis")]
        return names

    def lyrics(self) -> list:
        """Get lyrics list.

        :return list[str]:
        """
        texts: list = list()
        for track in self._tracks:
            for event in track:
                if all([event[1] == 0xFF, event[2] == 0x05]):
                    texts += [event[3].decode("sjis")]
        return texts

    def total_tick(self) -> int:
        """Count ticks.

        :return int:
        """
        result: int = 0
        for track in self._tracks:
            temp = track[len(track) - 1][0]
            result = temp if temp > result else result
        return result

    def _dequeue_as_midi_event(self, event_type: int, offset: int) -> tuple:
        """

        :param int event_type:
        :param int offset:
        :return tuple:
        """
        param = event_type >> 4
        channel = event_type & 0xF
        midi_event: list = list()
        if param in [0x8, 0x9, 0xA, 0xB, 0xE]:
            value0, value1, offset = self._unpack(offset, ">" "BB")
            midi_event = [param, channel, value0, value1]
        elif param in [0xC, 0xD]:
            value, offset = self._unpack(offset, BYTE)
            midi_event = [param, channel, value]
        return (midi_event, offset)

    def _dequeue_as_meta_event(self, event_type: int, offset: int) -> tuple:
        """

        :param int event_type:
        :param int offset:
        :return tuple:
        """
        meta_type, length, offset = self._unpack(offset, ">" "BB")
        return (
            [event_type, meta_type, self._smf[offset : offset + length]],
            offset + length,
        )

    def _dequeue_as_sysex_event(self, event_type: int, offset: int) -> tuple:
        """

        :param int event_type:
        :param int offset:
        :return tuple:
        """
        length, offset = self._unpack(offset, BYTE)
        return ([event_type, self._smf[offset : offset + length]], offset + length)

    def _dequeue_event(self, offset: int) -> tuple:
        """

        :param int offset:
        :return tuple:
        """
        event_type: int
        event_type, offset = self._unpack(offset, BYTE)
        if self._is_status_byte(event_type):
            self._last_event_type = event_type
        else:
            """running status"""
            event_type = self._last_event_type
            offset -= 1

        if event_type == 0xFF:
            return self._dequeue_as_meta_event(event_type, offset)
        elif event_type in [0xF0, 0xF7]:
            return self._dequeue_as_sysex_event(event_type, offset)
        else:
            return self._dequeue_as_midi_event(event_type, offset)

    def _header_chunk(self) -> tuple:
        """<Header Chunk>, <Track Chunk>+ <- <Standard MIDI File>

        :return tuple: chunk type, length, format, ntrks, division
        """
        ckID, ckSize, format, ntrks, division, offset = self._unpack(0, HEADER_CHUNK)
        return ([ckID.decode(), ckSize, format, ntrks, division], offset)

    def _is_status_byte(self, value: int) -> bool:
        """Find out if it's a status byte.

        :param int value:
        :return bool: True is status byte, False is data byte.
        """
        return True if value & 0x80 else False

    def _delta_time(self, offset: int) -> tuple:
        """<delta-time>, <event>+ <- <MTrk event>

        :param int offset: unpack start position
        :return tuple[int, int]: delta-time and new unpack start position
        """
        delta_time: int = 0
        temp: int
        while True:
            temp, offset = self._unpack(offset, BYTE)
            delta_time = temp & 0x7F
            while self._is_status_byte(temp):
                temp, offset = self._unpack(offset, BYTE)
                delta_time = (temp & 0x7F) + (delta_time << 7)
            return (delta_time, offset)

    def _unpack(self, offset: int, format: Union[str, bytes]) -> tuple:
        """Wrap function unpack_from() of 'module struct' module.

        :param int offset: unpack start position
        :param str format: Format strings describe the unpack data layout
        :return tuple: unpack data and new unpack start position
        """
        return (
            *struct.unpack_from(format, self._smf, offset),
            offset + struct.calcsize(format),
        )


if __name__ == "__main__":
    print(__file__)
