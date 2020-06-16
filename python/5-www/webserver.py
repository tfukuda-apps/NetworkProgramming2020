import socket
import signal

# キーボードからの[ctrl]+[c]を非同期で受付
signal.signal(signal.SIGINT, signal.SIG_DFL)

# 待受に使うIPアドレスとポート番号
MY_ADDRESS = ""
MY_PORT = 50000
# 受信用バッファサイズ
BUFSIZE = 1024
# HTTP Response
statusline = "HTTP/1.1 200 OK\r\n"
blank_line = "\r\n"
contents = "<!DOCTYPE html>\n<HTML><HEAD><META CHARSET='UTF-8'><BODY>"
contents += "いいよ～"
contents += "</BODY></HTML>"

# ソケットを作成
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 自分の情報をソケットに登録
sock.bind((MY_ADDRESS, MY_PORT))
# ソケットを待ち受け状態にする
sock.listen()

while True:
    # 接続要求→受理
    sock_c, addr = sock.accept()

    # HTTP Requestの受信
    req = sock_c.recv(BUFSIZE)
    print(req.decode("UTF-8"))

    try:
        sock_c.sendall(statusline.encode("UTF-8"))
        sock_c.sendall(blank_line.encode("UTF-8"))
        sock_c.sendall(contents.encode("UTF-8"))
    except:
        print("failed to sendall()")

    sock_c.close()

# 待ち受け用ソケットを閉じる
sock.close()
