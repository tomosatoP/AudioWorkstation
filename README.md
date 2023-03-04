# AudioWorkstation
USB MIDI 鍵盤を繋げて、ピアノ風の演奏を楽しみたいなぁ
### 機能
- MIDI Synthesizer
- メトローム
- Standard MIDI File 伴奏
### 構成
- ハードウェア
    - Raspberry Pi 4 Model B/4GB (Raspberry Pi OS with desktop 64bit)
    - microSD card 32GB 
    - 4.3inch DSI LCD with case (Waveshare 18645)
    - USB-DAC (Sharkoon GAMING DAC PRO S)
    - USB-MIDI Keyborad (未定)
- ソフトウェア
    - jackd2 version 1.9.17
    - fluidsynth version 2.1.7
    - python version 3.9.2
    - kivy version 2.1.0
---
## 準備
~~~sh
# 日本語フォント
~ $ sudo apt -y install fonts-ipaexfont
# jack, fluidsynth
~ $ sudo apt -y install jackd pulseaudio-module-jack fluidsynth libasound2-dev
~~~
## Kivyと依存関係のインストール(アプリ開発用)
方法1 (window用のbackendしか必要ないなら、これでOK？)

https://kivy.org/doc/stable/gettingstarted/installation.html#installing-kivy-s-dependencies
~~~sh
(venv) ~/AudioWorkstation $ python3 -m pip install "kivy[dev,base,sdl2]" kivy-example
~~~
方法2

https://kivy.org/doc/stable/installation/installation-rpi.html#install-python-rpi
~~~sh
~ $ sudo apt -y install pkg-config libgl1-mesa-dev libgles2-mesa-dev libgstreamer1.0-dev gstreamer1.0-plugins-{bad,base,good,ugly} gstreamer1.0-alsa libmtdev-dev xclip xsel libjpeg-dev
~ $ sudo apt -y install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev
(venv) ~/AudioWorkstation $ python3 -m pip install "kivy[dev,base]" kivy-example
~~~