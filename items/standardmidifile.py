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
        self._tracks = list()
        self._last_event_type = None
    
        self.header, queue = self._header_chunk(smf_bytes)

        for _ in range(self.header[3]):
            ckID, ckSize = self._unpac(queue, CKDR)
            queue_track = queue[struct.calcsize(CKDR):struct.calcsize(CKDR) + ckSize]
            queue = queue[struct.calcsize(CKDR) + ckSize:]

            current_time = int(0)
            list_event = list()
            while queue_track:
                delta_time, queue_track = self._delta_time(queue_track)
                event, queue_track = self._dequeue_event(queue_track)
                current_time += delta_time
                list_event.append([current_time, *event])
            
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

    def _dequeue_as_midi_event(self, data:bytes) -> tuple:
        event_type, = self._unpac(data, '>''B')
        param = event_type >> 4
        channel = event_type & 0xF
        if any([param == 0x8, param == 0x9, param == 0xA, param == 0xB, param == 0xE]):
            dummy, value0, value1 = self._unpac(data, '>''BBB')
            return([param, channel, value0, value1], data[3:])
        elif any([param == 0xC, param == 0xD]):
            dummy, value, = self._unpac(data, '>''BB')
            return([param, channel, value], data[2:])

    def _dequeue_as_meta_event(self, data:bytes) -> tuple:
        event_type, meta_type, length = self._unpac(data, '>''BBB')
        data = data[struct.calcsize('>''BBB'):]
        return([event_type, meta_type, data[0:length]], data[length:])

    def _dequeue_as_sysex_event(self, data:bytes) -> tuple:
        event_type, length = self._unpac(data, '>''BB')
        data = data[struct.calcsize('>''BB'):]
        return([event_type, data[0:length]], data[length:])

    def _dequeue_event(self, data:bytes) -> tuple:
        event_type, = self._unpac(data, BYTE)
        if self._is_status_byte(event_type):
            self._last_event_type = event_type
        else:
            ''' running status '''
            event_type = self._last_event_type
            data = struct.pack('>''B', event_type) + data

        if event_type == 0xFF:
            return(self._dequeue_as_meta_event(data))
        elif any([event_type == 0xF0, event_type == 0xF7]):
            return(self._dequeue_as_sysex_event(data))
        else:
            return(self._dequeue_as_midi_event(data))

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
