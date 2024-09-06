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

def receive_and_echo():
    while True:
        # Seeed Studioからのデータを受信
        if ser.in_waiting > 0:
            command = ser.read(ser.in_waiting).decode()  # 受信データをデコード
            print(f"Received: {command}")
            
            # 受信したコマンドをそのままSeeed Studioに送り返す
            ser.write(command.encode())  # エンコードして返信
            print(f"Sent back: {command}")

        time.sleep(3)  # 待機時間を少し挟む

if __name__ == "__main__":
    receive_and_echo()
