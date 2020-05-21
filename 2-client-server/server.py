import socket
import signal

# キーボードからの[ctrl]+[c]を非同期で受付
signal.signal(signal.SIGINT, signal.SIG_DFL)

# 待受に使うIPアドレスとポート番号
MY_ADDRESS = ""
MY_PORT = 50000
# 受信用バッファサイズ
BUFSIZE = 256

# ソケットを作成
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 自分の情報をソケットに登録
sock.bind((MY_ADDRESS, MY_PORT))
# ソケットを待ち受け状態にする
sock.listen()

while True:
    # 接続要求→受理
    sock_c, addr = sock.accept()

    # メッセージの送信
    msg = "hello!"
    try:
        sock_c.sendall(msg.encode("UTF-8"))
    except:
        print("sendall function failed.")

    # メッセージの受信＆表示
    data = sock_c.recv(BUFSIZE)
    print(data.decode("UTF-8"))

    # 通信用ソケットを閉じる
    sock_c.close()

# 待ち受け用ソケットを閉じる
sock.close()
