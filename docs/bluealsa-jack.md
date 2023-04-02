# Using BlueALSA with the JACK Audio Connection Kit
https://github.com/Arkq/bluez-alsa/wiki/Using-BlueALSA-with-the-JACK-Audio-Connection-Kit

## jackからALSAのバックエンドとしてBlueALSAに接続
~~~sh
jackd -r -d alsa -P bluealsa -n 3 -S -o 2
~~~
|||
|--|--|
|-r|Do not request real-time scheduling<br>(optional - will also work without this)|
|-d alsa|Use the ALSA backend|
|-P bluealsa|Use the most recently connected BlueALSA playback device.<br>You can also choose a specific device with `-P bluealsa:XX:XX:XX:XX:XX:XX`|
|-n 3|Use an ALSA buffer of 3 periods.<br>A smaller buffer is sure to produce underruns.|
|-o 2|Create 2 output channels|
|-S|Use S16_LE sample format|
|||

## ALSAプラグインを回避して、jackで再生処理
~~~diff
~ $ nano /etc/asound.conf
+ pcm.bt-headphones {
+ 	type bluealsa
+ 	device XX:XX:XX:XX:XX:XX
+ 	profile a2dp
+ }
+ ctl.bt-headphones {
+ 	type bluealsa
+ }
~~~
~~~sh
jackd -r -d alsa -P bt-headphones -n 3 -o 2
~~~