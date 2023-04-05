# Name Hint
|iface|NAME|DECS|IOID|
|---|---|---|---|
|ctl|sysdefault|Default control device|None|
|ctl|hw|Direct control device|None|
|ctl|bluealsa|Bluetooth Audio Control Device|None|
|ctl|arcam_av|Arcam-AV Amplifier|None|
|ctl|oss|None|None|
|ctl|pulse|None|None|
|ctl|linkbuds-aac|Bluetooth Headphones|Output|
|ctl|hw:CARD=Headphones|bcm2835 Headphones<br>Direct control device|None|
|ctl|hw:CARD=vc4hdmi0|vc4-hdmi-0<br>Direct control device|None|
|ctl|hw:CARD=vc4hdmi1|vc4-hdmi-1<br>Direct control device|None|
|pcm|null|Discard all samples (playback) or generate zero samples (capture)|None|
|pcm|lavrate|Rate Converter Plugin Using Libav/FFmpeg Library|None|
|pcm|samplerate|Rate Converter Plugin Using Samplerate Library|None|
|pcm|speexrate|Rate Converter Plugin Using Speex Resampler|None|
|pcm|bluealsa|Bluetooth Audio|None|
|pcm|jack|JACK Audio Connection Kit|None|
|pcm|oss|Open Sound System|None|
|pcm|pulse|PulseAudio Sound Server|None|
|pcm|upmix|Plugin for channel upmix (4,6,8)|None|
|pcm|vdownmix|Plugin for channel downmix (stereo) with a simple spacialization|None|
|pcm|linkbuds-aac|Bluetooth Headphones|Output|
|pcm|hw:CARD=Headphones,DEV=0|bcm2835 Headphones, bcm2835 Headphones<br>Direct hardware device without any conversions|Output|
|pcm|plughw:CARD=Headphones,DEV=0|bcm2835 Headphones, bcm2835 Headphones<br>Hardware device with all software conversions|Output|
|pcm|sysdefault:CARD=Headphones|bcm2835 Headphones, bcm2835 Headphones<br>Default Audio Device|Output|
|pcm|dmix:CARD=Headphones,DEV=0|bcm2835 Headphones, bcm2835 Headphones<br>Direct sample mixing device|Output|
|pcm|usbstream:CARD=Headphones|bcm2835 Headphones<br>USB Stream Output|None|
|pcm|hw:CARD=vc4hdmi0,DEV=0|vc4-hdmi-0, MAI PCM i2s-hifi-0<br>Direct hardware device without any conversions|Output|
|pcm|plughw:CARD=vc4hdmi0,DEV=0|vc4-hdmi-0, MAI PCM i2s-hifi-0<br>Hardware device with all software conversions|Output|
|pcm|sysdefault:CARD=vc4hdmi0|vc4-hdmi-0, MAI PCM i2s-hifi-0<br>Default Audio Device|Output|
|pcm|hdmi:CARD=vc4hdmi0,DEV=0|vc4-hdmi-0, MAI PCM i2s-hifi-0<br>HDMI Audio Output|Output|
|pcm|dmix:CARD=vc4hdmi0,DEV=0|vc4-hdmi-0, MAI PCM i2s-hifi-0<br>Direct sample mixing device|Output|
|pcm|usbstream:CARD=vc4hdmi0|vc4-hdmi-0<br>USB Stream Output|None|
|pcm|hw:CARD=vc4hdmi1,DEV=0|vc4-hdmi-1, MAI PCM i2s-hifi-0<br>Direct hardware device without any conversions|Output|
|pcm|plughw:CARD=vc4hdmi1,DEV=0|vc4-hdmi-1, MAI PCM i2s-hifi-0<br>Hardware device with all software conversions|Output|
|pcm|sysdefault:CARD=vc4hdmi1|vc4-hdmi-1, MAI PCM i2s-hifi-0<br>Default Audio Device|Output|
|pcm|hdmi:CARD=vc4hdmi1,DEV=0|vc4-hdmi-1, MAI PCM i2s-hifi-0<br>HDMI Audio Output|Output|
|pcm|dmix:CARD=vc4hdmi1,DEV=0|vc4-hdmi-1, MAI PCM i2s-hifi-0<br>Direct sample mixing device|Output|
|pcm|usbstream:CARD=vc4hdmi1|vc4-hdmi-1<br>USB Stream Output|None|
|rawmidi|virtual|None|None|
|seq|default|Default sequencer device|None|
|seq|hw|None|None|