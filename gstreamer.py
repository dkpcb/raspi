
# /home/pi/nrc_pkg/scriptに置く


# import gi
# from datetime import datetime
# from gi.repository import Gst, GObject

# # GStreamerを初期化
# Gst.init(None)

# def generate_filename():
#     """タイムスタンプを使ってファイル名を生成"""
#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     filename = f"/home/pi/videos/output_{timestamp}.h264"
#     return filename

# def run_gstreamer_pipeline():
#     """GStreamerパイプラインを実行"""
#     filename = generate_filename()
    
#     # GStreamerパイプラインの定義
#     pipeline_str = f"""
#     v4l2src device=/dev/video0 ! videoconvert ! video/x-raw,format=I420,width=640,height=480,framerate=30/1 ! tee name=t ! queue ! x264enc tune=zerolatency bitrate=2000 speed-preset=superfast ! rtph264pay ! udpsink host=192.168.10.100 port=5000 t. ! queue ! x264enc tune=zerolatency bitrate=2000 speed-preset=superfast ! h264parse ! filesink location={filename}
#     """
    
#     # GStreamerパイプラインを作成
#     pipeline = Gst.parse_launch(pipeline_str)

#     # パイプラインの実行
#     pipeline.set_state(Gst.State.PLAYING)

#     # メインループを開始して、GStreamerの状態を監視
#     loop = GObject.MainLoop()
    
#     try:
#         print(f"Streaming and recording... File: {filename}")
#         loop.run()
#     except KeyboardInterrupt:
#         print("Stopping...")
#     finally:
#         # パイプラインを停止
#         pipeline.set_state(Gst.State.NULL)
        


# gst_my_plugin.py

### 必要ライブラリのインポート ###
import gi
gi.require_version('Gst', '1.0')
gi.require_version('GstBase', '1.0')
gi.require_version('GstAudio', '1.0')

from gi.repository import Gst, GLib, GObject, GstBase, GstVideo, GstAudio

### 自作プラグインのクラスを宣言 ###
class GstMyPlugin(GstBase.BaseTransform):
    """
    作成するプラグインのタイプによって継承するクラスを変える

    BaseSrc: srcパッドだけが必要なプラグイン
    BaseSink: sinkパッドだけが必要なプラグイン
    BaseTransform: sink, srcが両方必要なプラグイン
    """

    ### Gstreamerプラグインの基本記述情報
    __gstmetadata__ = (
        "MyPlugin",  # Plugin name
        "Filter",    # Plugin Klass
                     #  - Source
                     #  - Sink
                     #  - Filter
                     #  - Effect
                     #  - Demuxer
                     #  - Muxer
                     #  - Decoder
                     #  - Encoder
                     #  - Mixer
                     #  - Converter
                     #  - Analyzer
                     #  - Control
                     #  - Extracter
                     #  - Formatter
                     #  - Connector
        "my plugin", # Plugin description
        "dai_guard <dai_guard@gmail.com>"  # Author information
    )

    ### パッドのCapabirity情報を記述する
    __gsttemplates__ = (
        Gst.PadTemplate.new(
            "src",
            Gst.PadDirection.SRC,
            Gst.PadPresence.ALWAYS,
            Gst.Caps.from_string(f"video/x-raw,format={FORMATS},width=[1,2147483647],height=[1,2147483647]")),
            .
            .
        )

    ### プラグインのproperty情報を記述する
    __gproperties__ = {
        "property_name": (
            GObject.TYPE_INT64,  # Data type
            "property_name",     # Nickname 
            "description",       # Description
            "1",                 # min value
            GLib.MAXINT,         # max value
            100,                 # default value
            GObject.ParamFlags.READWRITE, # parameter flags
        ),
        .
        .
    }

    ### 以下の関数は親クラスにオーバーライドされる
    ### コンストラクタ
    def __init__(self):
        ...
    ### プロパティの値を取得
    def do_get_property(self, prop):
        ...
    ### プロパティの値をセット
    def do_set_property(self, prop, value):
        ...
    ### 入力したバッファに対して出力バッファを作成する
    def do_transform(self, inbuf, outbuf):
        ...
    ### sinkが呼ばれた際に実行するバッファリングしょり
    def do_generate_output(self):
        ...
    ### capabilityのsink側とsrc側の情報を変化させる
    def do_transform_caps(self, direction, caps, filter_):
        ...
    ### capabilityのsink側とsrc側に固定の情報を流す
    def do_fixate_caps(self, direction, caps, othercaps):
        ...
    ### capabilityのsink側とsrc側を任意の値に設定する
    def do_set_caps(self, icaps, ocaps):
        ...

# 自作プラグインを登録する
GObject.type_register(GstMyPlugin)
__gstelementfactory__ = ("gst_my_plugin", Gst.Rank.NONE, GstMyPlugin)

