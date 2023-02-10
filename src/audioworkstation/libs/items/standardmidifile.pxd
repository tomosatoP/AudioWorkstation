#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''Directives are not available because of the absence of 'import cython'.'''

cdef class StandardMidiFile:

    cdef int _last_event_type
    cdef list _header
    cdef list _tracks
    cdef bytes _smf

    cpdef list channels_preset(self)
    cpdef str title(self)
    cpdef list instruments(self)
    cpdef list lyrics(self)
    cpdef int total_tick(self)

    cdef tuple _dequeue_as_midi_event(self, int event_type, int offset)
    cdef tuple _dequeue_as_meta_event(self, int event_type, int offset)
    cdef tuple _dequeue_as_sysex_event(self, int event_type, int offset)
    cdef tuple _dequeue_event(self, int offset)
    # cdef int event_type
    cdef tuple _header_chunk(self)
    
    cdef bint _is_status_byte(self, int value)
    cdef tuple _delta_time(self, int offset)
    # cdef int delta_time
    # cdef int temp

    cdef tuple _unpack(self, int offset, str format)