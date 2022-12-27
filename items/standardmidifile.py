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

FOURCC = '>''4s'
CKDR = FOURCC + 'L'
HEADER_CHUNK = CKDR + 'HHH'
BYTE = '>''B'

class StandardMidiFile():

    def __init__(self, smf_bytes: bytes) -> None:
        self.header = list()
        self.tracks = list()
        self.channels = [[]] * 16
        self._last_event_type = None

        self.header, data = self._header_chunk(smf_bytes)
        for i in range(self.header[3]):
            ckID, ckSize, = self._unpac(data, CKDR)
            track = data[struct.calcsize(CKDR):struct.calcsize(CKDR) + ckSize]
            data = data[struct.calcsize(CKDR) + ckSize:]

            total_time = int(0)
            list_event = list()
            while track:
                delta_time, track = self._delta_time(track)
                list_data, track = self._event(track)
                total_time += delta_time
                list_event.append([total_time, *list_data])
            
            self.tracks += [list_event]

    def channels_preset(self):
        for track in self.tracks:
            for event in track:
                if event[1] == 0xC:
                    self.channels[event[2]] = event[3]
        print(self.channels)


    def title(self) -> str:
        for event in self.tracks[0]:
            if all([event[1] == 0xFF, event[2] == 0x03]):
                return(event[3].decode('sjis'))
        return('-')

    def instruments(self):
        names = list()
        for track in self.tracks:
            for event in track:
                if all([event[1] == 0xFF, event[2] == 0x04]):
                    names += [event[3].decode('sjis')]
        return(names)

    def lyrics(self):
        texts = list()
        for track in self.tracks:
            for event in track:
                if all([event[1] == 0xFF, event[2] == 0x05]):
                    texts += [event[3].decode('sjis')]
        return(texts)

    def _midi_event(self, data:bytes) -> tuple:
        event_type, = self._unpac(data, '>''B')
        param = event_type >> 4
        channel = event_type & 0xF
        if any([param == 0x8, param == 0x9, param == 0xA, param == 0xB, param == 0xE]):
            dummy, value0, value1 = self._unpac(data, '>''BBB')
            return([param, channel, value0, value1], data[3:])
        elif any([param == 0xC, param == 0xD]):
            dummy, value, = self._unpac(data, '>''BB')
            return([param, channel, value], data[2:])

    def _meta_event(self, data:bytes) -> tuple:
        event_type, meta_type, length = self._unpac(data, '>''BBB')
        data = data[struct.calcsize('>''BBB'):]
        return([event_type, meta_type, data[0:length]], data[length:])

    def _sysex_event(self, data:bytes) -> tuple:
        event_type, length = self._unpac(data, '>''BB')
        data = data[struct.calcsize('>''BB'):]
        return([event_type, data[0:length]], data[length:])

    def _event(self, data:bytes) -> tuple:
        event_type, = self._unpac(data, BYTE)
        if self._is_status_byte(event_type):
            self._last_event_type = event_type
        else:
            ''' running status '''
            event_type = self._last_event_type
            data = struct.pack('>''B', event_type) + data

        if event_type == 0xFF:
            return(self._meta_event(data))
        elif any([event_type == 0xF0, event_type == 0xF7]):
            return(self._sysex_event(data))
        else:
            return(self._midi_event(data))

    def _header_chunk(self, data:bytes) -> tuple:
        ''' <Header Chunk>, <Track Chunk>+ <- <Standard MIDI File> '''
        ckID, ckSize, format, ntrks, division = self._unpac(data, HEADER_CHUNK)
        return([ckID.decode(), ckSize, format, ntrks, division], data[struct.calcsize(HEADER_CHUNK):])

    def _is_status_byte(self, value: bytes) -> bool:
        return(True if value & 0x80 else False)
    
    def _delta_time(self, data: bytes) -> tuple:
        ''' <delta-time>, <event>+ <- <MTrk event> '''
        while True:
            delta_time = 0
            temp, = self._unpac(data, BYTE)
            delta_time = temp & 0x7F
            data = data[struct.calcsize(BYTE):]
            while self._is_status_byte(temp):
                temp, = self._unpac(data, BYTE)
                delta_time = (temp & 0x7f) + (delta_time << 7)
                data = data[struct.calcsize(BYTE):]
            return(delta_time, data)

    def _unpac(self, data: bytes, format:str) -> tuple:
        return(struct.unpack_from(format, data[0: struct.calcsize(format)]))


if __name__ == '__main__':
    print('standardmidifile')
