# all cards
|iface|NAME|DECS|IOID|
|---|---|---|---|
|ctl|sysdefault|Default control device|None|
|ctl|default|None|None|
|ctl|hw|Direct control device|None|
|ctl|arcam_av|Arcam-AV Amplifier|None|
|ctl|oss|None|None|
|ctl|pulse|None|None|
|ctl|hw:CARD=Headphones|bcm2835 Headphones<br>Direct control device|None|
|ctl|hw:CARD=S|Sharkoon Gaming DAC Pro S<br>Direct control device|None|
|ctl|hw:CARD=vc4hdmi0|vc4-hdmi-0<br>Direct control device|None|
|ctl|hw:CARD=vc4hdmi1|vc4-hdmi-1<br>Direct control device|None|
|pcm|null|Discard all samples (playback) or generate zero samples (capture)|None|
|pcm|default|Playback/recording through the PulseAudio sound server|None|
|pcm|lavrate|Rate Converter Plugin Using Libav/FFmpeg Library|None|
|pcm|samplerate|Rate Converter Plugin Using Samplerate Library|None|
|pcm|speexrate|Rate Converter Plugin Using Speex Resampler|None|
|pcm|jack|JACK Audio Connection Kit|None|
|pcm|oss|Open Sound System|None|
|pcm|pulse|PulseAudio Sound Server|None|
|pcm|upmix|Plugin for channel upmix (4,6,8)|None|
|pcm|vdownmix|Plugin for channel downmix (stereo) with a simple spacialization|None|
|pcm|hw:CARD=Headphones,DEV=0|bcm2835 Headphones, bcm2835 Headphones<br>Direct hardware device without any conversions|Output|
|pcm|plughw:CARD=Headphones,DEV=0|bcm2835 Headphones, bcm2835 Headphones<br>Hardware device with all software conversions|Output|
|pcm|sysdefault:CARD=Headphones|bcm2835 Headphones, bcm2835 Headphones<br>Default Audio Device|Output|
|pcm|dmix:CARD=Headphones,DEV=0|bcm2835 Headphones, bcm2835 Headphones<br>Direct sample mixing device|Output|
|pcm|usbstream:CARD=Headphones|bcm2835 Headphones<br>USB Stream Output|None|
|pcm|hw:CARD=S,DEV=0|Sharkoon Gaming DAC Pro S, USB Audio<br>Direct hardware device without any conversions|None|
|pcm|plughw:CARD=S,DEV=0|Sharkoon Gaming DAC Pro S, USB Audio<br>Hardware device with all software conversions|None|
|pcm|sysdefault:CARD=S|Sharkoon Gaming DAC Pro S, USB Audio<br>Default Audio Device|None|
|pcm|front:CARD=S,DEV=0|Sharkoon Gaming DAC Pro S, USB Audio<br>Front output / input|None|
|pcm|surround21:CARD=S,DEV=0|Sharkoon Gaming DAC Pro S, USB Audio<br>2.1 Surround output to Front and Subwoofer speakers|Output|
|pcm|surround40:CARD=S,DEV=0|Sharkoon Gaming DAC Pro S, USB Audio<br>4.0 Surround output to Front and Rear speakers|Output|
|pcm|surround41:CARD=S,DEV=0|Sharkoon Gaming DAC Pro S, USB Audio<br>4.1 Surround output to Front, Rear and Subwoofer speakers|Output|
|pcm|surround50:CARD=S,DEV=0|Sharkoon Gaming DAC Pro S, USB Audio<br>5.0 Surround output to Front, Center and Rear speakers|Output|
|pcm|surround51:CARD=S,DEV=0|Sharkoon Gaming DAC Pro S, USB Audio<br>5.1 Surround output to Front, Center, Rear and Subwoofer speakers|Output|
|pcm|surround71:CARD=S,DEV=0|Sharkoon Gaming DAC Pro S, USB Audio<br>7.1 Surround output to Front, Center, Side, Rear and Woofer speakers|Output|
|pcm|iec958:CARD=S,DEV=0|Sharkoon Gaming DAC Pro S, USB Audio<br>IEC958 (S/PDIF) Digital Audio Output|Output|
|pcm|dmix:CARD=S,DEV=0|Sharkoon Gaming DAC Pro S, USB Audio<br>Direct sample mixing device|Output|
|pcm|dsnoop:CARD=S,DEV=0|Sharkoon Gaming DAC Pro S, USB Audio<br>Direct sample snooping device|Input|
|pcm|usbstream:CARD=S|Sharkoon Gaming DAC Pro S<br>USB Stream Output|None|
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

# card 0
|iface|NAME|DECS|IOID|
|---|---|---|---|
|ctl|hw:CARD=Headphones|bcm2835 Headphones<br>Direct control device|None|
|pcm|hw:CARD=Headphones,DEV=0|bcm2835 Headphones, bcm2835 Headphones<br>Direct hardware device without any conversions|Output|
|pcm|plughw:CARD=Headphones,DEV=0|bcm2835 Headphones, bcm2835 Headphones<br>Hardware device with all software conversions|Output|
|pcm|sysdefault:CARD=Headphones|bcm2835 Headphones, bcm2835 Headphones<br>Default Audio Device|Output|
|pcm|dmix:CARD=Headphones,DEV=0|bcm2835 Headphones, bcm2835 Headphones<br>Direct sample mixing device|Output|
|pcm|usbstream:CARD=Headphones|bcm2835 Headphones<br>USB Stream Output|None|

# card 1
|iface|NAME|DECS|IOID|
|---|---|---|---|
|ctl|hw:CARD=S|Sharkoon Gaming DAC Pro S<br>Direct control device|None|
|pcm|hw:CARD=S,DEV=0|Sharkoon Gaming DAC Pro S, USB Audio<br>Direct hardware device without any conversions|None|
|pcm|plughw:CARD=S,DEV=0|Sharkoon Gaming DAC Pro S, USB Audio<br>Hardware device with all software conversions|None|
|pcm|sysdefault:CARD=S|Sharkoon Gaming DAC Pro S, USB Audio<br>Default Audio Device|None|
|pcm|front:CARD=S,DEV=0|Sharkoon Gaming DAC Pro S, USB Audio<br>Front output / input|None|
|pcm|surround21:CARD=S,DEV=0|Sharkoon Gaming DAC Pro S, USB Audio<br>2.1 Surround output to Front and Subwoofer speakers|Output|
|pcm|surround40:CARD=S,DEV=0|Sharkoon Gaming DAC Pro S, USB Audio<br>4.0 Surround output to Front and Rear speakers|Output|
|pcm|surround41:CARD=S,DEV=0|Sharkoon Gaming DAC Pro S, USB Audio<br>4.1 Surround output to Front, Rear and Subwoofer speakers|Output|
|pcm|surround50:CARD=S,DEV=0|Sharkoon Gaming DAC Pro S, USB Audio<br>5.0 Surround output to Front, Center and Rear speakers|Output|
|pcm|surround51:CARD=S,DEV=0|Sharkoon Gaming DAC Pro S, USB Audio<br>5.1 Surround output to Front, Center, Rear and Subwoofer speakers|Output|
|pcm|surround71:CARD=S,DEV=0|Sharkoon Gaming DAC Pro S, USB Audio<br>7.1 Surround output to Front, Center, Side, Rear and Woofer speakers|Output|
|pcm|iec958:CARD=S,DEV=0|Sharkoon Gaming DAC Pro S, USB Audio<br>IEC958 (S/PDIF) Digital Audio Output|Output|
|pcm|dmix:CARD=S,DEV=0|Sharkoon Gaming DAC Pro S, USB Audio<br>Direct sample mixing device|Output|
|pcm|dsnoop:CARD=S,DEV=0|Sharkoon Gaming DAC Pro S, USB Audio<br>Direct sample snooping device|Input|
|pcm|usbstream:CARD=S|Sharkoon Gaming DAC Pro S<br>USB Stream Output|None|

# card 2
|iface|NAME|DECS|IOID|
|---|---|---|---|
|ctl|hw:CARD=vc4hdmi0|vc4-hdmi-0<br>Direct control device|None|
|pcm|hw:CARD=vc4hdmi0,DEV=0|vc4-hdmi-0, MAI PCM i2s-hifi-0<br>Direct hardware device without any conversions|Output|
|pcm|plughw:CARD=vc4hdmi0,DEV=0|vc4-hdmi-0, MAI PCM i2s-hifi-0<br>Hardware device with all software conversions|Output|
|pcm|sysdefault:CARD=vc4hdmi0|vc4-hdmi-0, MAI PCM i2s-hifi-0<br>Default Audio Device|Output|
|pcm|hdmi:CARD=vc4hdmi0,DEV=0|vc4-hdmi-0, MAI PCM i2s-hifi-0<br>HDMI Audio Output|Output|
|pcm|dmix:CARD=vc4hdmi0,DEV=0|vc4-hdmi-0, MAI PCM i2s-hifi-0<br>Direct sample mixing device|Output|
|pcm|usbstream:CARD=vc4hdmi0|vc4-hdmi-0<br>USB Stream Output|None|

# card 3
|iface|NAME|DECS|IOID|
|---|---|---|---|
|ctl|hw:CARD=vc4hdmi1|vc4-hdmi-1<br>Direct control device|None|
|pcm|hw:CARD=vc4hdmi1,DEV=0|vc4-hdmi-1, MAI PCM i2s-hifi-0<br>Direct hardware device without any conversions|Output|
|pcm|plughw:CARD=vc4hdmi1,DEV=0|vc4-hdmi-1, MAI PCM i2s-hifi-0<br>Hardware device with all software conversions|Output|
|pcm|sysdefault:CARD=vc4hdmi1|vc4-hdmi-1, MAI PCM i2s-hifi-0<br>Default Audio Device|Output|
|pcm|hdmi:CARD=vc4hdmi1,DEV=0|vc4-hdmi-1, MAI PCM i2s-hifi-0<br>HDMI Audio Output|Output|
|pcm|dmix:CARD=vc4hdmi1,DEV=0|vc4-hdmi-1, MAI PCM i2s-hifi-0<br>Direct sample mixing device|Output|
|pcm|usbstream:CARD=vc4hdmi1|vc4-hdmi-1<br>USB Stream Output|None|