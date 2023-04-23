#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Splash screen"""


import tkinter
from tkinter.ttk import Label


rootwindow = tkinter.Tk()
rootwindow.wm_title("AudioWorkstation")
rootwindow.wm_overrideredirect(True)
# attributes: -alpha, -fullscreen, -modified, -topmost, -transparent
rootwindow.wm_attributes("-topmost", True)

massage_text = tkinter.StringVar()
massage_text.set("読み込み中...")

message = Label(textvariable=massage_text, font=(None, "20"))
message.pack()

geo = "300x40+100+100"
rootwindow.wm_geometry(geo)
message.mainloop()
