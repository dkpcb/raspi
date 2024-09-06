import serial
import subprocess
import time
import os

# UARTの設定（/dev/serial1を使用）
serial_port = "/dev/serial1"  # GPIO14 (TXD) と GPIO15 (RXD) ピンを使用
baud_rate = 115200
timeout_duration = 10000  # タイムアウト時間（秒）

# シリアルポートを開く
ser = serial.Serial(serial_port, baudrate=baud_rate, timeout=1)

# ログファイルの設定
log_dir = "/home/pi/log"
log_file = os.path.join(log_dir, "uart_listener.log")

# ログディレクトリが存在しない場合、作成
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

#ログファイルにメッセージを書き込む
def log_message(message):
    with open(log_file, "a") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

#映像伝送とロギングを開始する処理
def start_video_and_logging():
    try:
        # start.pyスクリプトを引数付きで実行
        subprocess.run(["python3", "/home/pi/nrc_pkg/script/start.py", "0", "0", "JP"], check=True)
        log_message("start.py executed successfully.")
    except subprocess.CalledProcessError as e:
        log_message(f"Failed to execute start.py: {e}")

#映像伝送とロギングを終了する処理
def stop_video_and_logging():
    try:
        # stop.pyスクリプトを実行
        subprocess.run(["python3", "/home/pi/nrc_pkg/script/stop.py"], check=True)
        log_message("stop.py executed successfully.")
    except subprocess.CalledProcessError as e:
        log_message(f"Failed to execute stop.py: {e}")

def main():
    start_time = time.time()
    while True:
        # タイムアウトを確認
        elapsed_time = time.time() - start_time
        if elapsed_time > timeout_duration:
            log_message("Timeout reached. Stopping process.")
            break

        # XIAOからのコマンドを待機
        if ser.in_waiting > 0:
            command = ser.readline().decode('utf-8').strip()
            log_message(f"Received command: {command}")
            
            # "l" コマンドを受信した場合、確認応答として"l"を返送し、映像伝送とロギングを開始する
            if command == "l":
                log_message("Sending confirmation 'l'")
                ser.write(b"l\n")  # XIAOに"l"確認応答を送信
                log_message("Starting video transmission and logging.")
                start_video_and_logging()  # 映像伝送とロギングを開始
                log_message("Video transmission and logging started.")
            
            # "p" コマンドを受信した場合、確認応答として"p"を返送し、映像伝送とロギングを終了
            elif command == "p":
                log_message("Sending confirmation 'p'")
                ser.write(b"p\n")  # XIAOに"p"確認応答を送信
                log_message("Stopping video transmission and logging.")
                stop_video_and_logging()  # 映像伝送とロギングを終了
                log_message("Video transmission and logging stopped.")
                break
            
        else:
            log_message("No command received. Waiting...")

if __name__ == "__main__":
    main()




# import serial
# import subprocess
# import time
# import os

# # UARTの設定
# serial_port = "/dev/serial1"
# baud_rate = 115200
# timeout_duration = 10000  # タイムアウト時間（秒）

# # シリアルポートを開く
# ser = serial.Serial(serial_port, baudrate=baud_rate, timeout=1)

# # ログファイルの設定
# log_dir = "/home/pi/log"
# log_file = os.path.join(log_dir, "uart_listener.log")

# # ログディレクトリが存在しない場合、作成
# if not os.path.exists(log_dir):
#     os.makedirs(log_dir)

# #ログファイルにメッセージを書き込む
# def log_message(message):
#     with open(log_file, "a") as f:
#         f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

# #映像伝送とロギングを開始する処理
# def start_video_and_logging():
#     try:
#         # start.pyスクリプトを引数付きで実行
#         subprocess.run(["python3", "/home/pi/nrc_pkg/script/start.py", "0", "0", "JP"], check=True)
#         log_message("start.py executed successfully.")
#     except subprocess.CalledProcessError as e:
#         log_message(f"Failed to execute start.py: {e}")

# #映像伝送とロギングを終了する処理
# def stop_video_and_logging():
#     try:
#         # stop.pyスクリプトを実行
#         subprocess.run(["python3", "/home/pi/nrc_pkg/script/stop.py"], check=True)
#         log_message("stop.py executed successfully.")
#     except subprocess.CalledProcessError as e:
#         log_message(f"Failed to execute stop.py: {e}")

# def main():
#     start_time = time.time()
#     while True:
#         # タイムアウトを確認
#         elapsed_time = time.time() - start_time
#         if elapsed_time > timeout_duration:
#             log_message("Timeout reached. Stopping process.")
#             break

#         # XIAOからのコマンドを待機
#         if ser.in_waiting > 0:
#             command = ser.readline().decode('utf-8').strip()
#             log_message(f"Received command: {command}")
            
#             # "l" コマンドを受信した場合、確認応答として"l"を返送し、映像伝送とロギングを開始する
#             if command == "l":
#                 log_message("Sending confirmation 'l'")
#                 ser.write(b"l\n")  # XIAOに"l"確認応答を送信
#                 log_message("Starting video transmission and logging.")
#                 start_video_and_logging()  # 映像伝送とロギングを開始
#                 log_message("Video transmission and logging started.")
            
#             # "p" コマンドを受信した場合、確認応答として"p"を返送し、映像伝送とロギングを終了
#             elif command == "p":
#                 log_message("Sending confirmation 'p'")
#                 ser.write(b"p\n")  # XIAOに"p"確認応答を送信
#                 log_message("Stopping video transmission and logging.")
#                 stop_video_and_logging()  # 映像伝送とロギングを終了
#                 log_message("Video transmission and logging stopped.")
#                 break
            
#         else:
#             log_message("No command received. Waiting...")

# if __name__ == "__main__":
#     main()
