# bluealsa-plugins
https://github.com/Arkq/bluez-alsa/blob/master/doc/bluealsa-plugins.7.rst
## DESCRIPTION
BlueALSAは、ALSA alsa-lib APIを使用して、アプリケーションがBluetoothオーディオデバイスにアクセスすることを許可します。アプリケーションのユーザーは、Bluetoothスピーカー、ヘッドフォン、ヘッドセット、ハンズフリーデバイスを、あたかもローカルデバイスのように使用することができます。この統合は、PCMオーディオストリーム用とCTLボリュームコントロール用の2つのALSAプラグインによって実現されています。

## PCM PLUGIN
BlueALSA ALSA PCM プラグインは `bluealsa(8)` サービスと通信をします。ALSA PCM を独自の設定ファイル (例: ~/.asoundrc) で定義するために使うこともできますし、[あらかじめ定義された bluealsa PCM](#the-predefined-bluealsa-pcm) を使うこともできます。

### The Predefined bluealsa PCM
PCMプラグインを使用する最も簡単な方法は、あらかじめ定義されたALSAのPCMデバイスbluealsaを使用することです。このPCMデバイスの定義は`plug`タイプで、オーディオフォーマットの変換が必要な場合は、PCMによって自動的に行われます。DEV、PROFILE、CODEC、VOL、SOFTVOL、DELAY、SRVのパラメータを持ちます。これらのパラメータにはすべてデフォルトがあります。ALSA PCM 名の中のパラメータ値は、以下の構文で指定します：
~~~
bluealsa:DEV=01:23:45:67:89:AB,PROFILE=a2dp,CODEC=aac,VOL=60,SOFTVOL=no,DELAY=0,SRV=org.bluealsa
~~~

### PCM parameters
> DEV
>> _XX:XX:XX:XX:XX:XX_ という形式のデバイスBluetoothアドレスです。デバイス名やエイリアスはここでは有効ではありません。デフォルト値は **00:00:00:00:00** で、選択したプロファイルで最も最近接続されたデバイスが選択されます。

> PROFILE
>> **a2dp** または **sco** のいずれかを指定します。 **sco** は、ハンズフリー（HFP）またはヘッドセット（HSP）のいずれかのプロファイルを選択します（選択したデバイスで接続されている方）。デフォルトは **a2dp** です。

> CODEC
>> プロファイルで使用されるコーデックを指定します。デバイスとホストの間で接続が確立されたとき、BlueALSAはデバイスと利用可能な最良のコーデックをネゴシエートします。デフォルト値は **unchanged** で、PCMが既存のコーデック設定を使用するようになります。コーデック名は大文字と小文字を区別しないので、例えば **aptX** 、 **aptx** 、 **APTX** はすべて受け入れられます。指定されたコーデックが利用できない場合、プラグインは警告を発し、代わりにデフォルト値を使用します。<br><br>
BlueALSAは、HFP-HFノードからのHFPコーデックの変更をサポートしておらず、HFP-AGノードのみがHFPコーデックを変更することができます。<br><br>
oFonoはオーディオエージェントにコーデックの選択を許可していないため、BlueALSAをoFonoと組み合わせてHFP対応にする場合、本パラメータは影響を与えません。<br><br>
A2DPプロファイルでは、コーデック名とコロンで区切られた16進数の文字列として設定を追加することで、コーデックの「構成」を指定することも可能です。例：

    CODEC=aptx:4f0000000100ff

> VOL
>> PCMを開いたときの初期音量を指定します。デフォルト値は、PCMが既存の音量設定を使用するようになる**unchanged**です。値は、最大音量に対するパーセンテージの整数値[0-100]です。また、「-」を付けると消音(mute)、「＋」を付けると発音(unmute)になるように設定できます。PCMを閉じた状態では、音量は元の値に戻りません。例えば、初期音量を80%に設定し、このPCMでミュートが無効になっていることを確認する場合：

    VOL=80+
> SOFTVOL
>> このPCMに対するBlueALSAのソフトウェアボリューム機能の有効・無効を設定します。ソフトウェアボリュームの詳細については、`bluealsa(8)` のマニュアルページを参照してください。これはブーリアンオプション（値は**on**または**off**）ですが、PCMが既存のsoftvol値を使用するようになる特別な値**unchanged**も受け付けます。デフォルト値は **unchanged** です。

> DELAY
>> オーディオの同期を手動で調整するために、報告されたレイテンシー値に追加される整数値です。通常は必要なく、デフォルトは **0** です。

> SRV
>> TBlueALSAデーモンのD-Busサービス名です。デフォルトは **org.bluealsa** です。詳しくは `bluealsa(8)` を参照してください。通常は必要ありません。
### Setting Different Defaults
デフォルトは、例えば、変更したいものを独自の設定（~/.asoundrc.confなど）で定義することで上書きすることができます：
~~~
defaults.bluealsa.device "00:11:22:33:44:55"
defaults.bluealsa.profile "sco"
defaults.bluealsa.codec "cvsd"
defaults.bluealsa.volume "50+"
defaults.bluealsa.softvol off
defaults.bluealsa.delay 5000
defaults.bluealsa.service "org.bluealsa.source"
~~~
### Positional Parameters
ALSA では、引数を明示的に指定する代わりに、位置パラメーターとして指定することができます。位置パラメーターを使うときは、DEV、PROFILE、CODEC、VOL、SOFTVOL、DELAY、SRVという正しい順序で値を与えることが重要です。例えば、次のようになります：
~~~
bluealsa:01:23:45:67:89:AB,a2dp,unchanged,unchanged,unchanged,0,org.bluealsa
~~~
位置指定パラメータを使用する場合、デフォルトはid文字列の末尾にのみ暗示されるため、以下のようになります。
~~~
bluealsa:01:23:45:67:89:AB
~~~
は、上記のフルフォームと同等ですが
~~~
bluealsa:01:23:45:67:89:AB,a2dp,,80+
~~~
は許されない。

### Defining BlueALSA PCMs
ALSAのコンフィギュレーションで、独自のALSA PCMを定義することができます。そのためには、`bluealsa` タイプの PCM を定義する ALSA 設定ノードを作成します。この設定ノードには、以下のフィールドがあります：
~~~
pcm.name {
  type bluealsa     # Bluetooth PCM
  device STR        # Device address in format XX:XX:XX:XX:XX:XX
  profile STR       # Profile type (a2dp or sco)
  [codec STR]       # Preferred codec
  [volume STR]      # Initial volume for this PCM
  [softvol BOOLEAN] # Enable/disable BlueALSA's software volume
  [delay INT]       # Extra delay (frames) to be reported (default 0)
  [service STR]     # DBus name of service (default org.bluealsa)
}
~~~
プラグインが正しいBluetoothトランスポートを選択できるように、**device**と**profile**フィールドを指定する必要があります; 他のフィールドはオプションです。オプションのフィールドのデフォルト値は、この方法で定義された PCM の `defaults.bluealsa.*` という設定によって自動的に上書きされないことに注意してください; しかし、`@func refer` を使うことで設定のデフォルト値を参照できます (より詳しい情報は ALSA 設定ファイルの構文ドキュメントを参照してください)。

PCM定義の名前を選ぶとき、**pcm.bluealsa**という名前はbluez-alsaのインストールによってあらかじめ定義されています（上記の「The Predefined bluealsa PCM」を参照）ので、あなた自身のPCMデバイスの名前として使用するべきではありません。

**volume**フィールドは**string**型であるため、値をダブルクォートで囲む必要があることに注意する。各フィールドの詳細については、上記の「PCM パラメータ」セクションを参照してください。

PCMタイプ**bluealsa**とPCMに名付けた**bluealsa**を混同しないでください。この型は音声変換を行わないので、そのためには独自に定義したPCMを**plug**型でラップする必要があります；一方、定義済みのPCM **pcm.bluealsa**は**plug**型です。

### Name Hints
ALSAのガイドラインに従うアプリケーションは、alsa-lib namehints APIを使用して定義されたPCMのリストを取得します。このAPIを使ってBlueALSAのPCMを見えるようにするには、ALSAの設定に「hint」セクションを追加する必要がある。新しいPCMを定義した場合、ヒントは以下のようにPCMの設定項目に入ります：
~~~
pcm.bt-headphones {
    type plug
    slave.pcm {
        type bluealsa
        device "00:11:22:33:44:55"
        profile "a2dp"
    }
    hint {
        show on
        description "My Bluetooth headphones"
    }
}
~~~
ここで、`aplay -L`を使用すると、その出力に以下のものが含まれます：
~~~
# aplay -L
bt-headphones
    My Bluetooth headphones
#
~~~
[定義済みのbluealsa PCM](#defining-bluealsa-pcms)を使用している場合は、~/.asoundrcファイルに次のように「namehint」エントリーを作成することができます：
~~~
namehint.pcm {
    mybluealsadevice "bluealsa:DEV=00:11:22:33:44:55,PROFILE=a2dp|My Bluetooth headphones"
}
~~~
そして、play -Lで表示されます。
~~~
# aplay -L
bluealsa:DEV=00:11:22:33:44:55,PROFILE=a2dp
    My Bluetooth headphones
~~~
v1.2.3.2 以前の alsa-lib バージョンでは、namehint パーサーのバグにより、**namehint.pcm** エントリーが
~~~
namehint.pcm {
    mybluealsadevice "bluealsa:DEV=00:11:22:33:44:55,PROFILE=a2dp|DESCMy Bluetooth headphones"
}
~~~
(パイプ記号の後、説明文の前に**DESC**というキーワードがあることに注意)。

このヒントがあれば、PCMはキャプチャとプレイバックの両方のデバイスとしてリストアップされます。そのため、`arecord -L`もそれをリストアップします。HFP/HSPデバイスの場合は概ねこれでOKですが、A2DPデバイスの場合はCaptureのみ（携帯電話など）、Playbackのみ（Bluetoothスピーカーなど）であることがほとんどです。ALSA 設定ファイルの文書化されていない構文を使って、ヒントの記述を使ってリストを一方向にのみ限定することが可能です。

hint.descriptionの値が **|IOIDInput**で終わる場合、PCMはCaptureデバイスのリストにのみ表示され、**|IOIDOutput**で終わる場合、PCMはPlaybackデバイスのリストにのみ表示されます。

そこで、上の例を次のように修正することができます：
~~~
pcm.bt-headphones {
    type plug
    slave.pcm {
        type bluealsa
        device "00:11:22:33:44:55"
        profile "a2dp"
    }
    hint {
        show on
        description "My Bluetooth headphones|IOIDOutput"
    }
}
~~~
もしくは
~~~
namehint.pcm {
    mybluealsadevice "bluealsa:DEV=00:11:22:33:44:55,PROFILE=a2dp|My Bluetooth headphones|IOIDOutput"
}
~~~
これで、`play -L`の出力は以前と全く同じになりますが、`arecord -L`はbt-headphonesを出力に含めない。

namehint.pcm メソッドを使う場合、キー（上の例では mybluealsadevice）はユニークでなければなりませんが、それ以外は使われません。値の文字列の最初の部分、パイプ | シンボルの前は、PCM を識別するために ALSA アプリケーションに渡す文字列です (例えば `aplay -D ...` といったように)。パイプ記号の後の次のセクションは、ユーザーに提示される説明文です。オプションの **|IOID** セクションは、アプリケーションに与えられる説明には含まれません。
## CTL PLUGIN
BlueALSA ALSA CTLプラグインは、ALSA CTL（ミキサーデバイス）を独自の設定ファイル（例：~/.asoundrc）で定義することができますが、bluez-alsaプロジェクトに含まれている定義済みの設定を使うこともできます。<br>
BlueALSA CTLデバイスには関連するサウンドカードがないため、`alsamixer`のF6メニューに表示されません。以下のように`alsamixer`を起動することで選択することができます。
~~~
alsamixer -D bluealsa
~~~
または、F6メニューの "enter device name ... "を選択し、"Device Name "ボックスに "bluealsa "と入力してください。

CTLには、DefaultモードとSingle Deviceモードの2つの動作モードがあります。
### Default Mode
このモードでは、デバイスが接続されると、ミキサーはそのための新しいコントロールを作成し、デバイスが切断されると、ミキサーはそのコントロールを削除します。`alsamixer(1)`はこれらの変更を動的に表示します。

コントロール名は、デバイスのBluetoothエイリアスと、制御されるPCMのプロファイルタイプ（「A2DP」または「SCO」）、またはバッテリーレベルインジケーターの「Battery」という単語を組み合わせて作成されます。接続された2つ以上のデバイスが同じエイリアスを持つ場合、ユニークにするために名前にインデックス番号が追加されます。

デバイスのBluetooth "alias"は、デフォルトで "name"と同じです。名前は、デバイスのメーカーが定義した文字列で、ファームウェアに組み込まれています。通常、2つの同じデバイスが同じ名前を持つことになります。"alias"はBlueZが作成し、ホストコンピュータのローカルに保存されます。そのため、必要に応じて、`bluetoothctl(1)`などのツールを使ってエイリアスを変更し、ユニークなものにすることができます。メーカーはデバイスに長い名前を付ける傾向があるので、エイリアスはデバイスに短い"nickname"を付けるのにも便利です。

このデフォルトモードは alsamixer でうまく機能しますが、いくつかのアプリケーションに適さない制限もあります。特に

- デバイスの別名が一意でない場合、それぞれに関連するインデックス番号を事前に予測することは容易ではありません。したがって、PCMとそのボリュームコントロールをプログラム的に関連付けることは困難です。
- コントロールのalsa-lib実装の結果として、1つのBluetoothデバイスが接続または切断されると、ミキサー内のすべてのデバイスからすべてのコントロールを削除し、新しいセットを作成する必要があります。これは、アプリケーションによって保持されているポインタを無効にし、アプリケーションのクラッシュを引き起こす可能性があります。(ハードウェアのサウンドカードには、ランダムに現れたり消えたりするコントロールはないので、多くの、あるいはほとんどのアプリケーションは、これに対処するために正しくプログラムされていません)。
### Single Device Mode
BlueALSA CTLは、指定された1つのデバイスのコントロールのみを提示する代替モードも実装しています。この場合、コントロール名は、制御されるPCMのプロファイルタイプ（「A2DP」または「SCO」）または単語「Battery」だけです。インデックスサフィックスやデバイスエイリアスは一切必要ありません。これにより、デフォルトモードの2つの主要な問題が即座に克服されます。

シングルデバイスモードは、例えばALSAデバイスIDの引数としてデバイスのBluetoothアドレスを含めることで実現します：
~~~
alsamixer -D bluealsa:00:11:22:33:44:55
~~~
シングルデバイスモードとデフォルトモードの顕著な違いは、ミキサーを開いたときにデバイスが接続されていない場合と、ミキサーを開いているときにデバイスが切断された場合です。

デフォルトモードの場合、デバイスが接続されていなくてもミキサーは開きますが、コントロールは表示されません。シングルデバイスモードでは、オープンリクエストはエラーメッセージを表示して失敗します。

同様に、デフォルトモードでは、デバイスが切断されると、ミキサーは開いたままですが、コントロールのセットを削除して、切断されたデバイスを含まない新しいコントロールセットを作成します。デバイスが残っていない場合、この新しいセットは空となります。デバイスが再接続されると、ミキサーは新たに接続されたデバイスを含む新しいコントロールセットを再び作成します。

シングルデバイスモードでは、デバイスが切断されると、ミキサーは終了します。alsamixerアプリケーションは、関連するデバイスやコントロールがない状態で実行し続けますが、デバイスが再接続されてもミキサーを自動的に開くことはありません。ユーザーはF6で新しいデバイスを開くことができます。

特別なケースとして、単一デバイスのミキサーをアドレス00:00:00:00:00:00でオープンすることができます。これは、ミキサーが開かれた時点で最も新しく接続されたデバイスのコントロールを持つミキサーを作成します。一度作成されたミキサーは、実際のデバイスのアドレスで開かれた場合と同じように動作します：その後、別のデバイスが接続されても、新しいデバイスに変わることはありません。
### The Predefined bluealsa CTL
bluealsa CTLには、DEV、EXT、BAT、BTT、DYN、SRVというパラメータがあります。すべてのパラメータにデフォルトがあります。
#### CTL Parameters
> DEV
>> XX:XX:XX:XX:XX:XXという形式のデバイスBluetoothアドレスです。デバイス名やエイリアスはここでは有効ではありません。デフォルト値は**FF:FF:FF:FF:FF:FF**で、接続されているすべてのデバイスからコントロールを選択します（上記の[Default Mode](#default-mode)を参照）。また、最近接続されたデバイスを選択する特別なアドレス**00:00:00:00:00:00**を受け入れる。

> EXT
>> プラグインに、コーデックとソフトウェアの音量選択のコントロールを含めるようにする。値が**yes**の場合、これらの追加コントロールが含まれます。デフォルトは**no**です。ソフトボリュームコントロールは「Mode」と呼ばれ、「software」と「pass-through」の値をとり、再生コントロールはインデックス0、キャプチャコントロールはインデックス1です。ソフトボリューム設定の詳細については `bluealsa(8)` を、コーデックコントロールの詳細については、以下の [NOTES](#notes) セクションの [Codec selection](#codec-selection) を参照してください。

> BAT
>> デバイスがサポートしている場合、プラグインに（読み取り専用の）バッテリー残量インジケータを含めるようにします。値が **yes** の場合、バッテリーインジケーターが有効になり、それ以外の値の場合、バッテリーインジケーターは無効になります。デフォルトは **no** です。

> BTT
>>コントロールエレメント名にBluetoothトランスポートタイプ（例："-SNK "または"-HFP-AG"）を付加します。[Default Mode](#default-mode)で使用する場合、Bluetoothデバイス名に使用できる文字数が少なくなるため、デフォルト値は **no** です。<br><br>
1つのBluetooth機器に複数のA2DPまたはHFP/HSPプロファイルが接続されている場合、稀にその機器のコントロールエレメント名が一意にならないことがあります。これは ALSA High Level Control Interface を使用するアプリケーション（例：`amixer` や `alsamixer`）にとって問題となる可能性があります。そのようなアプリケーションはエラーを報告するか、単にクラッシュします。この問題は、BTTパラメータを **yes** に設定することで回避することができます。

> DYN
>> 「動的」な操作を可能にします。プラグインは、プロファイルが接続または切断されると、コントロールを追加および削除します。これは通常の動作であるため、デフォルト値は「**yes**」です。この引数はデフォルトモードでは無視されます。このモードでは操作は常に動的です。コントロールの動的な追加や削除を処理するようにプログラムされていないアプリケーションもあり、そのようなイベントが発生したときに失敗する可能性があります。このようなアプリケーションのシングルデバイスモードでこの引数を **no** に設定すると、そのような失敗から保護することができます。動的操作が無効な場合、プラグインはコントロールを追加または削除することはありません。単一のプロファイルが切断された場合、関連するボリュームコントロールは非アクティブな状態、すなわち、その値とplayback/capture switchを0に設定した読み取り専用になります。

> SRV
>>BlueALSAデーモンのD-Busサービス名です。デフォルトは **org.bluealsa** です。詳しくは `bluealsa(8)` を参照してください。

デフォルト値は、ALSAの設定で上書きすることができます、例：
~~~
defaults.bluealsa.ctl.device "00:11:22:33:44:55"
defaults.bluealsa.ctl.battery "no"
defaults.bluealsa.ctl.bttransport "no"
defaults.bluealsa.ctl.dynamic "yes"
defaults.bluealsa.ctl.extended "no"
~~~
### Defining BlueALSA CTLs
ALSAコンフィギュレーションで独自のALSA CTLを定義することができます。そのためには、`bluealsa`というタイプのCTLを定義するALSA設定ノードを作成します。この設定ノードには以下のフィールドがあります：
~~~
ctl.name {
  type bluealsa     # Bluetooth PCM
  [device STR]      # Device address (default "FF:FF:FF:FF:FF:FF")
  [extended STR]    # Include additional controls (yes/no, default no)
  [battery STR]     # Include battery level indicator (yes/no, default no)
  [bttransport STR] # Append BT transport to element names (yes/no, default no)
  [dynamic STR]     # Enable dynamic operation (yes/no, default yes)
  [service STR]     # D-Bus name of service (default "org.bluealsa")
}
~~~
全てのフィールド（typeを除く）はオプションである。各フィールドの詳細については、上記の「CTLパラメータ」セクションを参照してください。上記のPCMの定義と同様に、オプションフィールドのデフォルト値はプラグインにハードコードされています; これらはコンフィギュレーション`defaults.bluealsa.`settingsによって上書きされることはありません。
# NOTES
### Codec selection
HFPゲートウェイノードで使用する場合、接続後、コーデックが選択されるまで、HFP PCMで短い遅延が発生することがあります。この遅延は、通常2秒未満です。この時間帯はPCMプラグインを開くことができず、"Resource temporarily unavailable"（EAGAIN）で失敗します。
### Codec switching
BlueALSAトランスポートで使用されているコーデックを変更すると、そのトランスポート上で動作しているPCMが終了します。したがって、コーデックコントロールを使用することは、望ましくない結果をもたらす可能性があります。残念ながら `alsamixer(1)` UI は、列挙型のための独立したピックリストを表示しないので、このコントロールを使用してコーデックのリストを参照するだけで、異なるコーデックが表示されるたびに、実際にコーデック変更要求を発行します。これは理想的なことではないので、このコントロールタイプを `alsamixer(1)` と共に使用することは推奨されません。しかし、このコントロールタイプは、`amixer(1)`のような他のミキサーアプリケーションではうまく機能します。

BlueALSAは、HFP-HFノードからHFPコーデックを変更することをサポートしていないことに注意してください。
### Transport acquisition
プロファイルのオーディオ接続は、デバイスが接続してもすぐに確立されるわけではありません。A2DPソースデバイス、またはHFP/HSPゲートウェイデバイスは、最初にプロファイルトランスポートを「獲得」する必要があります。

BlueALSA PCMプラグインがソースA2DPまたはゲートウェイHFP/HSPノードで使用されている場合、 **bluealsa(8)** はプラグインがPCMを開始すると、自動的にトランスポートを獲得し、オーディオ転送を開始します。

A2DPシンクまたはHFP/HSPターゲットノードで使用される場合、 **bluealsa(8)** はリモートデバイスがトランスポートを獲得するのを待つ必要があります。この待ち時間の間、PCMプラグインはデバイスの「クロック」が停止しているかのように振る舞い、poll()イベントを生成せず、アプリケーションはPCMへの書き込みや読み込みの際にブロックされることになる。ファイルからオーディオを再生したり、ファイルにオーディオを記録するアプリケーションでは、これは通常問題にはなりませんが、他のデバイスとBlueALSAデバイスの間でストリーミングする場合、これは非常に大きなレイテンシー（遅延）につながり、他のデバイスのアンダーランやオーバーランを引き起こすかもしれません。
# FILES
**/etc/alsa/conf.d/20-bluealsa.conf**

BlueALSAのデバイス設定ファイルです。ALSA追加設定、bluealsa PCMとCTLデバイスを定義しています。