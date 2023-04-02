# PulseAudio integration
https://github.com/Arkq/bluez-alsa/wiki/PulseAudio-integration
## Using BlueALSA and PulseAudio Together
[PulseAudio](https://www.freedesktop.org/wiki/Software/PulseAudio/) は、特にデスクトップインストール用の、事実上のLinux標準オーディオサーバです。多くのLinuxディストリビューションのデスクトップは、完全な機能を提供するために、PulseAudioを必要とします。

PulseAudioは独自のBluetoothオーディオ実装を持っており、多くの一般的な使用シナリオではこれで十分です。何らかの理由でPulseAudioを使用する必要がある場合は、この統合を試みる前に、少なくとも内部のBluetoothオーディオの実装を試すことをお勧めします。逆に、PulseAudioが不要な場合は、BluetoothオーディオにBlueALSAを使用し、PulseAudioを全く実行しないことをお勧めします。

もちろん、両方のサービスを実行する必要がある場合も稀にあるかもしれません。このWiki記事では、2つのサービスを統合的に使用する1つの方法について説明します。この方法は「実験的」であり、多くの妥協と制限を伴うものであると考えるべきでしょう。

Bluezでは、Bluetoothプロファイルのプロバイダとして登録できるサービスは1つだけなので、PulseaudioをBlueALSAと組み合わせて使用するには、PulseAudio bluetoothモジュールを無効化する必要があります。
## Preparing PulseAudio for use with BlueALSA
### Disable PulseAudio bluetooth modeles
PulseAudio bluetooth モジュールを無効にするには、3 つの方法があります。
#### 1. Uninstall the module packages
多くのディストリビューションでは、PulseAudio bluetoothモジュールが別のパッケージとして提供されているため、これらのパッケージをアンインストールすることが最も簡単な解決策です。例えば、Ubuntuの場合
~~~
~ $ sudo apt purge --auto-remove pulseaudio-module-bluetooth
~~~
#### 2. Remove the modules from the PulseAudio configuration
略
#### 3. Unload the PulseAudio bluetooth modules at runtime
略
### Remove PulseAudio ALSA default config
PulseAudio はそれ自身をデフォルトの ALSA PCM デバイスとしてインストールします。これを実現するために、ユーザー自身のPCM定義に干渉する可能性のある "フック "関数を使用します。多くのBlueALSAの設定はALSA設定の特定のエントリに依存しているので、"フック "機能を削除することが推奨されます。これは、シンボリックリンクを削除することによって行うことができます：
~~~
~ $ sudo unlink /etc/alsa/conf.d/99-pulse.conf
~~~
もし、PulseAudioをALSAのデフォルトのPCMデバイスとして使い続けたい場合は、~/.asoundrcファイルに次の行を追加することで可能です：
~~~
pcm.!default pulse
~~~
## Adding BlueALSA Devices as PulseAudio Sinks / Sources
上記の変更により、PulseAudioと同時にBlueALSAサービスを実行することが可能になりました。アプリケーションは、Bluetoothデバイスを使用するために、ALSA APIを使用してALSAに直接接続する必要があり、PulseAudioはそれらを見ることができません。そのため、PulseAudio APIを使用するように設定されているアプリケーション（デスクトップのボリュームコントロールパネルのほとんどを含む）は、Bluetoothオーディオを使用することができません。多くのシステムではこれで十分かもしれませんが、このセクションはオプションで、PulseAudio API経由でBlueALSAデバイスを使用する必要がある場合（例えばUbuntuのFirefoxなど）にのみ関係します。

PulseAudio API経由でBlueALSA PCMを表示するには、コンフィグレーションの準備をもう少し行い、関連モジュールをPulseAudioに手動でロードする必要があります。次の3つのステップでこの手順を説明します。
### 1. Define ALSA PCM for BlueALSA with no conversions
PulseAudio が必要なオーディオフォーマットの変換を内部で行うようにし、alsa-lib "plug" や他の alsa プラグインを使用しないことをお勧めします。これは、特に libasound バージョン 1.1.2 または 1.1.3 を使用している場合に重要で、そうしないと PulseAudio デーモンがデッドロックになります。これを実現する簡単な方法は、適切な ALSA の設定ディレクトリに **21-bluealsa-raw.conf** というファイルを作成することです。
- /usr/share/alsa/alsa.conf.d/21-bluealsa-raw.conf ( alsa-lib version <= 1.1.6 )
- /etc/alsa/conf.d/21-bluealsa-raw.conf ( alsa-lib version >= 1.1.7 )
そのファイルに次のように記述します：略
### 2. Configure PulseAudio to suspend on idle
_このステップは、A2DPとHFP/HSPの両方のシンク（またはA2DPとHFP/HSPの両方のソース）を提供するデバイスを使用する場合にのみ必要です。_

特に設定しない限り、PulseAudioはロードされた各BlueALSA PCMデバイスを直ちに開き、保持します。これは、A2DPとSCO PCMの両方をサポートするデバイスの問題を引き起こす可能性があります。PCMをロードしたまま開かないようにする唯一の方法は、それを「サスペンド」することです。しかし、ほとんどのPulseAudio GUIツール（`pavucontrol`を含む）では、ユーザーがシンクやソースを手動でサスペンドしたりアンサスペンドしたりすることができません。これを回避するには、十分に低いタイムアウトで「suspend-on-idle」機能を有効にする必要があります。この機能を有効にするLinuxディストリビューションもあれば、そうでないものもあります。PulseAudioインスタンスにこのモジュールがロードされているかどうかを確認するには、次のように入力します：
~~~
pactl list modules
~~~
をクリックし、module-suspend-on-idleのエントリーを探してください：
~~~
Module #20
	Name: module-suspend-on-idle
	Argument: timeout=5
	Usage counter: n/a
	Properties:
		module.author = "Lennart Poettering"
		module.description = "When a sink/source is idle for too long, suspend it"
		module.version = "11.1"
~~~
モジュール番号、およびその他のパラメータ値は異なる場合があります。

モジュールがロードされている場合は、"Argument: "パラメータを確認します。A2DPからSCOに切り替わるときに、その時間の無音が発生するので、低いタイムアウト値が必要です。Argumentが空白の場合、デフォルトのタイムアウトは5秒です。

モジュールがロードされていない場合、またはタイムアウトを変更する必要がある場合は、ファイル /etc/pulse/default.pa を編集する必要があります。として、エントリーを追加します（または既存のエントリーを編集します）：
~~~
### Automatically suspend sinks/sources that become idle for too long
load-module module-suspend-on-idle timeout=2
~~~
#### _Important Note:_
`pavucontrol` はデフォルトで各デバイスのボリュームメーターを表示し、`pavucontrol` の実行中にデバイスがサスペンドされることを防ぎます。音量計を無効にし、`pavucontrol` 実行中の自動サスペンド機能を有効にするには、pavucontrol **Configuration** タブで、左下の「音量計を表示する」のチェックを外してください。
### 3. Create sink and / or source objects
PulseAudioで使用する各Bluetoothデバイスは、シンク、ソース、またはその両方として、個別に追加する必要があります。1つのデバイスでA2DPとSCOの両方のプロファイルを使用したい場合は、それらも個別に追加する必要があります。

デバイスを追加する方法は、`module-alsa-sink` または `module-alsa-source` モジュールに適切なパラメータをロードすることです。後でデバイスを削除するために、デバイスに割り当てられたモジュールのインデックスを記録しておくと便利です。ユーティリティ `pactl` は、正常に終了するとそのインデックスを返します。これらのモジュールのパラメータの完全なリストは、ここで見ることができます：
https://www.freedesktop.org/wiki/Software/PulseAudio/Documentation/User/Modules/

module-alsa-sinkとmodule-alsa-sourceが使用するデフォルトでは、PulseAudioが一度に何秒も応答しなくなることがあるので、「fragments」と「fragment_size」モジュールパラメータを明示的に設定する必要がある。最初の推測として `fragments=1`、`fragment_size=960` を試してみて、そこから実験することをお勧めします。

`sink_properties` または `source_properties` パラメータを適宜使用し、`pavucontrol` などのグラフィカルツールやデスクトップのサウンドコントロールアプリケーション/ウィジェットで表示される説明文に使用するために、デバイスにユーザーフレンドリーな説明を与えることは有用です。

デフォルトは "audio-card "ですが、"audio-speakers-bluetooth", "audio-headphones-bluetooth", "audio-headset-bluetooth", "phone-bluetooth" または単に "bluetooth" を使用することも可能でしょう。実際に利用できるアイコンは、デスクトップのディストリビューションに依存します。

PulseAudioに追加する前に、まずデバイスを接続する必要があります。

例えば、再生（シンク）デバイスをロードし、その内部名（`pactl` や `pacmd` などのコマンドラインツールで使用）を設定し、そのユーザーフレンドリーな説明とアイコンを設定し、割り当てられたモジュールインデックスを記録するには、次のように入力します：
~~~
MODULE=$(pactl load-module module-alsa-sink device='bluealsa_raw:DEV=XX:XX:XX:XX:XX,PROFILE=a2dp' fragments='1' fragment_size='960' sink_name=MyFriendlyName sink_properties="device.description='My Friendly Description'device.icon_name=Audio-speakers-bluetooth")
~~~
（デバイス欄には上記で定義した "bluealsa_raw "を使用し、説明欄にはスペース文字をバックスラッシュでエスケープする必要があることに注意してください。プロパティ設定とプロパティの間にスペースを残さないでください。）

PulseAudioからデバイスを削除するには、次のように入力します。
~~~
pactl unload-module $MODULE
~~~
キャプチャ（ソース）デバイスの場合も、コマンドの「sink」の代わりに「source」を使用する以外は同じ手順となります：
~~~
MODULE=$(pactl load-module module-alsa-source device='bluealsa_raw:DEV=XX:XX:XX:XX:XX:XX,PROFILE=a2dp' fragments='1' fragment_size='960' source_name=MyFriendlyName source_properties="device.description='My\ Friendly\ Description'device.icon_name=phone-bluetooth")
~~~
## Automating The Addition Of BlueALSA Devices to PulseAudio
org.bluealsa からの D-Bus ObjectManager イベントをリッスンし、BlueALSA PCM の追加と削除に対応して上記の `pactl` コマンドを起動するサービスを実行することで、上記の手順を自動化することが可能である。次のスクリプト例は、BlueALSAのユーティリティbluealsa-cliを使用してイベント監視を実行する方法を示しています。
> このスクリプトは BlueALSA リリース v4.0.0 で導入された bluealsa-cli ユーティリティの機能を必要とするため、それ以前のリリースでは動作しないでしょう。BlueALSAをソースからビルドする際には、必ずconfigureオプション--enable-cliを追加してbluealsa-cliユーティリティをビルドしてください。
### 1. Create D-Bus service
（スクリプトは省略）

このスクリプトは、rootではなく、通常のユーザーとして実行する必要があります。

**同じデバイス上でA2DPシンクからSCOシンクにストリームを切り替える場合、ストリームが再開するまでに数秒の沈黙があることに注意してください。SCO再生は、PulseAudioによってA2DPデバイスがサスペンドされたときにのみ開始されるからです。**
### 2. Run the D-Bus servie whenever PulseAudio in running
デスクトップセッション内でPulseAudioを実行し、systemdを使用している場合、上記のスクリプト（または独自の改良サービス）をsystemdユーザーサービスとして有効にすることで、デスクトップにログインするたびに起動させることができます。

例えば、上記のスクリプトを /usr/local/bin/bluepulse.bash としてインストールする場合、以下の systemd サービスファイルを保存します：

**/usr/local/lib/systemd/user/bluepulse.service**
~~~
[Unit]
Description=BlueALSA PulseAudio Integration
BindsTo=pulseaudio.service
After=pulseaudio.service

[Service]
Type=simple
ExecStart=/usr/local/bin/bluepulse.bash
RestartSec=2
Restart=on-failure

[Install]
WantedBy=pulseaudio.service
~~~
このサービスを利用したい各ユーザーは、次のようにしてログイン時の起動を有効にします：
~~~
systemctl --user enable bluepulse.service
~~~
Systemdは、pulseaudioが起動するとそのユーザーのbluepulseサービスを開始し、pulseaudioが停止するとそれを停止するようになりました。
