import serial
import time
import os
import subprocess

# シリアルポートの設定
ser = serial.Serial(
    port='/dev/serial0',  # 使用するポート（Raspberry PiのUARTポート）
    baudrate=9600,      # ボーレート（Seeed Studioと同じにする）
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1             # タイムアウト
)

# ログファイルの設定
log_dir = "/home/pi/log"
log_file = os.path.join(log_dir, "uart.log")

# ログディレクトリが存在しない場合、作成
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# ログファイルにメッセージを書き込む関数
def log_message(message):
    with open(log_file, "a") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

# 映像伝送とロギングを開始する処理
# def start_video_and_logging():
#     try:
#         # start.pyスクリプトを引数付きで実行
#         subprocess.Popen(["python3", "/home/pi/nrc_pkg/script/start.py", "0", "0", "JP"], check=True)
#         log_message("start.py executed successfully.")
#     except subprocess.CalledProcessError as e:
#         log_message(f"Failed to execute start.py: {e}")

# # 映像伝送とロギングを終了する処理
# def stop_video_and_logging():
#     try:
#         # stop.pyスクリプトを実行
#         subprocess.Popen(["python3", "/home/pi/nrc_pkg/script/stop.py"], check=True)
#         log_message("stop.py executed successfully.")
#     except subprocess.CalledProcessError as e:
#         log_message(f"Failed to execute stop.py: {e}")


def start_video_and_logging():
    try:
        # start.pyスクリプトをバックグラウンドで実行
        subprocess.run("python3 /home/pi/nrc_pkg/script/start.py 0 0 JP &", shell=True, check=True)
        log_message("start.py executed in background with & successfully.")
    except subprocess.CalledProcessError as e:
        log_message(f"Failed to execute start.py in background: {e}")

# 映像伝送とロギングを終了する処理
def stop_video_and_logging():
    try:
        # stop.pyスクリプトを実行（通常実行）
        subprocess.run(["python3", "/home/pi/nrc_pkg/script/stop.py"], check=True)
        log_message("stop.py executed successfully.")
    except subprocess.CalledProcessError as e:
        log_message(f"Failed to execute stop.py: {e}")
        
# カメラが認識されているか確認する処理
def check_camera():
    try:
        # カメラの状態を確認するコマンドを実行
        result = subprocess.run(["vcgencmd", "get_camera"], stdout=subprocess.PIPE, text=True)
        output = result.stdout.strip()
        log_message(f"Camera check output: {output}")
        
        # 出力に "supported=1 detected=1" が含まれている場合、カメラが認識されている
        if "supported=1" in output and "detected=1" in output:
            return "t"  # カメラが認識されている場合
        else:
            return "f"  # カメラが認識されていない場合
    except Exception as e:
        log_message(f"Error checking camera: {e}")
        return "ff"  # エラーの場合も認識されていないとする


# コマンドを受け取り処理する
def receive_commands():
    while True:
        if ser.in_waiting > 0:
            command = ser.read(ser.in_waiting).decode().strip()  # 受信データをデコード
            print(f"Received command: {command}")
            log_message(f"Received command: {command}")
            
            if command == 'l':
                start_video_and_logging()  # 映像伝送とロギング開始
                ser.write("l".encode())  # 確認コマンドを送信
                log_message("Sent confirmation: l")
            elif command == 'p':
                stop_video_and_logging()  # 映像伝送とロギング終了
                ser.write("p".encode())  # 確認コマンドを送信
                log_message("Sent confirmation: p")
            elif command == 's':
                camera_status = check_camera()  # カメラ認識状態を確認
                ser.write(camera_status.encode())  # 結果（T or F）をシリアルで送信
                log_message(f"Sent camera status: {camera_status}")
            else:
                print(f"Unknown command: {command}")
                log_message(f"Unknown command: {command}")

        time.sleep(0.1)  # 負荷軽減のため少し待機

if __name__ == "__main__":
    receive_commands()
