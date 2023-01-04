#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Purpose
    Analyze MIDI files according to SMF (Standard MIDI File) format
reference
    MIDI1.0規格書(日本語版98.1) ISBN4-8456-0348-9 C3055  http://www.amei.or.jp/
        2. MIDI 1.0
        4. スタンダードMIDIファイル1.0
'''

import struct
from pathlib import Path

FOURCC = '>''4s'
CKDR = FOURCC + 'L'
HEADER_CHUNK = CKDR + 'HHH'
BYTE = '>''B'

class StandardMidiFile():

    def __init__(self, smf:Path) -> None:
        self.header = list()
        self._tracks = list()
        self._last_event_type = None

        smf = smf.read_bytes()
    
        offset = int()
        self.header, offset = self._header_chunk(smf)

        for _ in range(self.header[3]):
            ckID, ckSize, offset = self._unpac(smf, offset, CKDR)

            current_time = int(0)
            list_event = list()
            while ckSize:
                ckSize += offset
                delta_time, offset = self._delta_time(smf, offset)
                current_time += delta_time

                event, offset = self._dequeue_event(smf, offset)
                list_event.append([current_time, *event])
                ckSize -= offset

            self._tracks += [list_event]

    def channels_preset(self):
        channels = [[]]*16
        for track in self._tracks:
            for event in track:
                if event[1] == 0xC:
                    channels[event[2]] = event[3]
        return(channels)

    def title(self) -> str:
        for event in self._tracks[0]:
            if all([event[1] == 0xFF, event[2] == 0x03]):
                return(event[3].decode('sjis'))
        return('-')

    def instruments(self):
        names = list()
        for track in self._tracks:
            for event in track:
                if all([event[1] == 0xFF, event[2] == 0x04]):
                    names += [event[3].decode('sjis')]
        return(names)

    def lyrics(self):
        texts = list()
        for track in self._tracks:
            for event in track:
                if all([event[1] == 0xFF, event[2] == 0x05]):
                    texts += [event[3].decode('sjis')]
        return(texts)

    def _dequeue_as_midi_event(self, smf:Path, event_type:bytes, offset:int) -> tuple:
        param = event_type >> 4
        channel = event_type & 0xF
        if any([param == 0x8, param == 0x9, param == 0xA, param == 0xB, param == 0xE]):
            value0, value1, offset = self._unpac(smf, offset, '>''BB')
            return([param, channel, value0, value1], offset)
        elif any([param == 0xC, param == 0xD]):
            value, offset = self._unpac(smf, offset, '>''B')
            return([param, channel, value], offset)

    def _dequeue_as_meta_event(self, smf:Path, event_type:bytes, offset:int) -> tuple:
        meta_type, length, offset = self._unpac(smf, offset, '>''BB')
        return(
            [event_type, meta_type, smf[offset: offset + length]],
            offset + length)

    def _dequeue_as_sysex_event(self, smf:Path, event_type:bytes, offset:int) -> tuple:
        length, offset = self._unpac(smf, offset, '>''B')
        return(
            [event_type, smf[offset: offset + length]],
            offset + length)

    def _dequeue_event(self, smf:Path, offset:int) -> tuple:
        event_type, offset = self._unpac(smf, offset, BYTE)
        if self._is_status_byte(event_type):
            self._last_event_type = event_type
        else:
            ''' running status '''
            event_type = self._last_event_type
            offset -= 1

        if event_type == 0xFF:
            return(self._dequeue_as_meta_event(smf, event_type, offset))
        elif any([event_type == 0xF0, event_type == 0xF7]):
            return(self._dequeue_as_sysex_event(smf, event_type, offset))
        else:
            return(self._dequeue_as_midi_event(smf, event_type, offset))

    def _header_chunk(self, smf:Path) -> tuple:
        ''' <Header Chunk>, <Track Chunk>+ <- <Standard MIDI File> '''
        ckID, ckSize, format, ntrks, division, offset = self._unpac(smf, 0, HEADER_CHUNK)
        return([ckID.decode(), ckSize, format, ntrks, division], offset)

    def _is_status_byte(self, value: bytes) -> bool:
        return(True if value & 0x80 else False)
    
    def _delta_time(self, smf:Path, offset:int) -> tuple:
        ''' <delta-time>, <event>+ <- <MTrk event> '''
        while True:
            delta_time = 0
            temp, offset = self._unpac(smf, offset, BYTE)
            delta_time = temp & 0x7F
            while self._is_status_byte(temp):
                temp, offset = self._unpac(smf, offset, BYTE)
                delta_time = (temp & 0x7f) + (delta_time << 7)
            return(delta_time, offset)

    def _unpac(self, smf:Path, offset:int, format:str) -> tuple:
        return(
            *struct.unpack_from(format, smf, offset),
            offset + struct.calcsize(format))


if __name__ == '__main__':
    print('standardmidifile')
