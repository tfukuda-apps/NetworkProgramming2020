import socket
import signal
# キーボードからの[ctrl]+[c]を非同期で受付
signal.signal(signal.SIGINT, signal.SIG_DFL)

# 接続先情報
HOST = input("ホスト名を入力:")
PORT = input("ポート番号を入力:")

# 受信用バッファサイズ
BUFSIZE = 1024

# ソケットを作成
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 接続
try:
    sock.connect((HOST, int(PORT)))
except:
    exit()

# HTTP Request
req_line = "GET / HTTP/1.1\r\n"
req_head = "Host: {}\r\n".format(HOST)
blank_line = "\r\n"

try:
    # HTTP Requestの送信
    sock.sendall(req_line.encode("UTF-8"))
    sock.sendall(req_head.encode("UTF-8"))
    sock.sendall(empty_line.encode("UTF-8"))

    # HTTP Responseの受信
    while True:
        data = sock.recv(BUFSIZE)
        if len(data) == 0:
            break
        print(data.decode("UTF-8"))

except:
    print("error")

# ソケットを閉じる
sock.close()

# http://tfukuda.s1009.xrea.com/
