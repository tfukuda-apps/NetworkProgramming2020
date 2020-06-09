import socket
import signal
# キーボードからの[ctrl]+[c]を非同期で受付
signal.signal(signal.SIGINT, signal.SIG_DFL)

# 接続先情報
HOST = "127.0.0.1"
PORT = 50000
# 受信用バッファサイズ
BUFSIZE = 256

# ソケットを作成
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 接続
sock.connect((HOST, PORT))

# メッセージの受信＆表示
data = sock.recv(BUFSIZE)
print(data.decode("UTF-8"))

# メッセージの送信
msg = input("message:")
try:
    sock.sendall(msg.encode("UTF-8"))
except:
    print("sendall function failed.")

# ソケットを閉じる
sock.close()
