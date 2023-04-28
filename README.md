# ![icon](image/audioworkstation.small.png) AudioWorkstation
USB MIDI 鍵盤を繋げて、ピアノ風の演奏を楽しむために。
### 機能
- MIDI Synthesizer 経由の USB MIDI 演奏
- メトローム
- Standard MIDI File による伴奏

![entry](image/entry.small.png)
![keyboard](image/keyboard.small.png)
![metronome](image/metronome.small.png)
![player](image/player.small.png)
### 構成
- ハードウェア
    - Raspberry Pi 4 Model B/4GB (Raspberry Pi OS with desktop 64bit)
    - microSD card 32GB 
    - DISPLAY
        - 4.3inch DSI LCD with case ([Waveshare 18645][1] )
    - AUDIO OUTPUT 
        - Headphones Jack
        - USB-DAC ([Sharkoon GAMING DAC PRO S][2] )
        - Bluetooth Headphones([SONY LinkBuds][4])
    - INPUT
        - USB-MIDI Keyborad ([M-AUDIO KEYSTATION49 MK3][3] )
- ソフトウェア
    - JACK Audio Connection Kit version 1.9.17
    - FluidSynth version 2.1.7
    - Python version 3.9.2
    - Kivy[base] version 2.1.0
---
## 準備
~~~sh
# 日本語フォント
~ $ sudo apt -y install fonts-ipaexfont
# jackd(jackd2) with qjackctl 
# fluidsynth with libfluidsynth2, qsynth, fluid-soundfont-gm)
~ $ sudo apt -y install jackd pulseaudio-module-jack fluidsynth
~~~
> Bluetoothデバイスへ音出しするには、[RaspberryPi4 - Bluetooth A2DP 接続](memorandum/bluetooth-devices.md)を参照
## インストール
~~~sh
~ $ python3 -m venv AudioWorkstation/venv --upgrade-deps
~ $ cd AudioWorkstation
~/AudioWorkstation $ source venv/bin/activate
(venv) ~/AudioWorkstation $ pip install -U git+https://github.com/tomosatoP/AudioWorkstation.git
(venv) ~/AudioWorkstation $ initialize
# Audioworkstation/sf2フォルダにsf2サウンドフォントファイルを設置
# Audioworkstation/midフォルダにSMF(StandardMidiFile)ファイルを設置
# sh venv/lib/python3.9/site-packages/audioworkstation/compile.sh
(venv) ~/AudioWorkstation $ deactivate
~~~
## 実行
~~~sh
~ $ cd AudioWorkstation
~/AudioWorkstation $ source venv/bin/activate
(venv) ~/AudioWorkstation $ python3 -m audioworkstation
# 終わったら
(venv) ~/AudioWorkstation $ deactivate
~~~
[API仕様書はこちら](https://tomosatop.github.io/AudioWorkstation/)
## アンインストール
~~~sh
~ $ rm -rf AudioWorkstation
~~~

[1]:https://www.waveshare.com/4.3inch-dsi-lcd-with-case.htm
[2]:https://ja.sharkoon.com/product/27415
[3]:https://m-audio.com/keystation-49-mk3
[4]:https://www.sony.jp/headphone/products/LinkBuds/