# RaspberryPi4 - Bluetooth A2DP 接続
## BlueALSA: Bluetooth Audio ALSA Backend
https://github.com/Arkq/bluez-alsa
https://joker1007.hatenablog.com/entry/2021/10/17/213109
### Install Required Tools and Essential Development Libraries
~~~sh
# build tools
~ $ sudo apt install automake libtool git build-essential pkg-config python3-docutils
# essential development libraries
~ $ sudo apt install libasound2-dev libbluetooth-dev libdbus-1-dev libglib2.0-dev libsbc-dev
# libraries for profile A2DP codec AAC
~ $ sudo apt install libfkd-aac2 libfdk-aac-dev
~~~
### Create onfigure script
~~~sh
~ $ git clone https://github.com/Arkq/bluez-alsa.git
~/bluez-alsa $ autoreconf --install --force
~~~
### Set configure options
~~~sh
~/bluez-alsa $ mkdir build
~/bluez-alsa/build $ ../configure [OPTION ...]
> --enable-aac: require libfdk-aac2, libfdk-aac-dev.
> --enable-systemd: none required.
> # --enable-cli: require libdbus-1-3, libdbus-1-dev.
> # --disable-aplay: 
~~~
### Build & install
~~~sh
~/bluez-alsa/build $ make
~/bluez-alsa/build $ sudo make install
~~~
### Update
~~~sh
~ $ autoreconf --install --force
~/bluez-alsa/build $ ../configure [OPTION ...]
~/bluez-alsa/build $ make clean
~/bluez-alsa/build $ make
~/bluez-alsa/build $ sudo make install
~~~
### Uninstall
~~~sh
~/bluez-alsa/build $ sudo make uninstall
~~~
### Add groups
~~~sh
~ $ sudo adduser --system --group --no-create-home bluealsa
~ $ sudo adduser --system --group --no-create-home bluealsa-aplay
~ $ sudo adduser bluealsa-aplay audio
~~~
### Files
|||
| --- | --- |
|設定|/etc/alsa/conf.d/20-bluealsa.conf<br>/etc/dbus-1/system.d/bluealsa.conf|
|systemd|/lib/systemd/system/bluealsa.service<br>/lib/systemd/system/bluealsa-aplay.service|
|binaries|/usr/lib/aarch64-linux-gnu/alsa-lib/*<br>/usr/bin/bluealsa<br>/usr/bin/bluealsa-aplay<br>/usr/bin/bluealsa-cli|
|||
## GUI でのペアリング
- deviceをペアリングモードにする
- RaspberyPi4をBluetooth"検出可能"にする
- 追加
- A2DP接続にするため、オーディオメニューから"device"を選択

## bluetoothctl でのペアリング
- deviceをペアリングモードにする
~~~
~ $ sudo bluetoothctl
[bluetooth]# show  # レシーバーの状態確認
[bluetooth]# power on  # "Powered on"にはなるが、"Powered yes"にするには？
[bluetooth]# pairable on
[bluetooth]# scan on -> [▯▯NEW▯▯] Device [device address] [device name]
[bluetooth]# scan off
[bluetooth]# pair [device address]
[[device name]]# paired-devices -> Device [device address] [device name]
[[device name]]# trust [device address]
[[device name]]# connect [device address]
[[device name]]# disconnect
~~~

## 接続テスト
~~~
~ $ aplay -D bluealsa:XX:XX:XX:XX:XX:XX /usr/share/sounds/alsa/Front_Center.wav
# 接続後にしばらくすると再生ができず、"hw params のインストールに失敗しました:"となる
~~~
## 設定変更
~~~diff
~ $ sudo ln -s /etc/alsa/conf.d/20-bluealsa.conf /usr/share/alsa/alsa.conf.d/20-bluealsa.conf
~ $ sudo nano /etc/dbus-1/system.d/bluetooth.conf
+   <policy user="bluealsa">
+     <allow send_destination="org.bluez"/>
+   </policy>
  
  </busconfig>

~ $ sudo nano /etc/dbus-1/system.d/bluealsa.conf
-     <allow send_destination="org.bluealsa"/>
+     <allow send_destination="org.bluealsa.sink"/>
+     <allow send_destination="org.bluealsa.source"/>

~ $ sudo nano /etc/asound.conf
+ defaults.bluealsa.interface "hci0"
+ defaults.bluealsa.device "XX:XX:XX:XX:XX:XX"
+ defaults.bluealsa.profile "a2dp"
+ defaults.bluealsa.delay 10000
+ 
+ pcm.bt-receiver {
+  type bluealsa
+   device "XX:XX:XX:XX:XX:XX"
+   profile "a2dp"
+ }
~~~
---
#### 関連ファイル
- [ ] ~/.asoundrc
- [ ] /etc/asound.conf
- [x] /etc/alsa/conf.d/20-bluealsa.conf
- [x] /etc/dbus-1/system.d/bluetooth.conf
- [x] /etc/dbus-1/system.d/bluealsa.conf
- [x] /etc/default/bluetooth
- [ ] /etc/default/bluez-alsa
- [x] /lib/systemd/system/blueatooth.service
- [x] /lib/systemd/system/blueatooth.target
- [x] /lib/systemd/system/bluealsa.service
- [x] /lib/systemd/system/bluealsa-aplay.service
- [ ] /usr/etc/alsa/conf.d
- [ ] /usr/etc/asound.conf

#### WAVファイル
/usr/share/sounds/alsa/Noise.wav<br>
/usr/share/sounds/alsa/Rear_Left.wav<br>
/usr/share/sounds/alsa/Rear_Center.wav<br>
/usr/share/sounds/alsa/Side_Left.wav<br>
/usr/share/sounds/alsa/Front_Center.wav<br>
/usr/share/sounds/alsa/Front_Right.wav<br>
/usr/share/sounds/alsa/Rear_Right.wav<br>
/usr/share/sounds/alsa/Front_Left.wav<br>
/usr/share/sounds/alsa/Side_Right.wav<br>