# 使い易くする為の覚書

### system update
~~~sh
~ $ sudo apt update
~ $ sudo full-upgrade -y
~ $ sudo autoremove -y
~ $ sudo reboot
~~~
### raspi-config 設定
~~~sh
~ $ sudo raspi-config
~~~
|1|2|3|4|
|---|---|---|---|
|1 System Options|S5 Boot / Auto Login|B4 Desktop Autologin||
||S6 Network at Boot|yes||
|5 Localisation Options|L1 Locale|[*] ja_jp.UTF-8||
||L2 Timezone|Asia|Tokyo|
### Wi-Fi を OFF
~~~diff
~ $ sudo nano /boot/config.txt
+  dtoverlay=disable-wifi
~~~
### ssh経由のKivy開発の為に
~~~diff
~ $ sudo nano /etc/profile
+  export DISPLAY=':0'
~~~
### python3, pip update
~~~sh
~ $ sudo apt -y install python3 python3-pip
~ $ sudo -H python3 -m pip install --upgrade pip
~~~
### package化 と 開発インストール
~~~sh
~ $ python3 -m venv AudioWorkstation/venv --upgrade-deps
~/AudioWorkstation $ . venv/bin/activate
(venv) ~AudioWorkstation $ pip install build
(venv) ~AudioWorkstation $ python3 -m build
(venv) ~AudioWorkstation $ pip install -e .
~~~
### ROM化
~~~sh
~ $ sudo raspi-config
~~~
|1|2|3|4|
|---|---|---|---|
|4 Performance Options|P3 Overlay File System|yes|yes|
