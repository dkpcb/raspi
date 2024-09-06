import serial
import time

# シリアルポートの設定
ser = serial.Serial(
    port='/dev/serial0',  # 使用するポート（Raspberry PiのUARTポート）
    baudrate=9600,      # ボーレート（Seeed Studioと同じにする）
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1             # タイムアウト
)

def send_command(cmd):
    ser.write(cmd.encode())  # コマンドをエンコードして送信
    print(f"Sent: {cmd}")

    time.sleep(0.1)  # 短い待機時間（シリアルデータを待つ）

    # 返信を受け取る
    if ser.in_waiting > 0:
        response = ser.read(ser.in_waiting).decode()  # デコードして返信を取得
        print(f"Received: {response}")

if __name__ == "__main__":
    while True:
        cmd = input("Enter a command to send: ")  # ユーザーからの入力を待つ
        send_command(cmd)
