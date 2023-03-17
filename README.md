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
    - kivy[base] version 2.1.0
---
## 準備
~~~sh
# 日本語フォント
~ $ sudo apt -y install fonts-ipaexfont
# jackd, fluidsynth
~ $ sudo apt -y install jackd pulseaudio-module-jack fluidsynth
~~~
## 仮想環境[venv]でインストール
~~~sh
~ $ git clone --depth 1 https://github.com/tomosatoP/AudioWorkstation.git
~ $ cd AudioWorkstation
~/AudioWorkstation $ python3 -m venv venv --upgrade-deps
~/AudioWorkstation $ source venv/bin/activate
(venv) ~/AudioWorkstation $ pip install .
(venv) ~/AudioWorkstation $ deactivate
~~~
## 仮想環境[venv]で実行
~~~sh
~ $ cd AudioWorkstation
~/AudioWorkstation $ source venv/bin/activate
(venv) ~/AudioWorkstation $ python3 -m audioworkstation
# 終わったら
(venv) ~/AudioWorkstation $ deactivate
~~~
## 仮想環境[venv]ごと削除
~~~sh
~ $ rm -rf AudioWorkstation
~~~
