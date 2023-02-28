# AudioWorkstation
USB MIDI 鍵盤を繋げて、ピアノ風の演奏を楽しみたいなぁ
### 機能
- MIDI Synthesizer
- メトローム
- Standard MIDI File 伴奏
### 構成
- ハードウェア
    - Raspberry Pi 4 Model B/4GB
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
必要なパッケージのインストール
~~~sh
# 日本語フォント
~ $ sudo apt -y install fonts-ipaexfont
# jack, fluidsynth
~ $ sudo apt -y install jackd pulseaudio-module-jack fluidsynth libasound2-dev
# Kivyに必要なパッケージ
~ $ sudo apt -y install pkg-config libgl1-mesa-dev libgles2-mesa-dev libgstreamer1.0-dev gstreamer1.0-plugins-{bad,base,good,ugly} gstreamer1.0-alsa libmtdev-dev xclip xsel libjpeg-dev
~ $ sudo apt -y install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev
~~~