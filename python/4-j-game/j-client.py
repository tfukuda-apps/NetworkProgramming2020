import socket
import signal
# キーボードからの[ctrl]+[c]を非同期で受付
signal.signal(signal.SIGINT, signal.SIG_DFL)

# 接続先情報
HOST = "127.0.0.1"
PORT = 50000
# 受信用バッファサイズ
CHARSET = "UTF-8"
BUFSIZE = 1024

# ソケットを作成
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 接続
sock.connect((HOST, PORT))

# ゲーム開始
# ルール等の受信
msg = sock.recv(BUFSIZE)
print(msg.decode(CHARSET))

while True:
    try:
        # まずは自分の手を決めて送信（入力の値を調べたほうが良い）
        mine = input("3で終了[0-3]:")
        sock.sendall(mine.encode(CHARSET))
        # 結果を受信・表示
        msg = sock.recv(BUFSIZE)
        print(msg.decode(CHARSET))
        if int(mine) == 3:
            print("サーバとの接続が切断されました")
            break
    except:
        sock.close()
        print("サーバとの接続が切断されました")
        break

# ソケットを閉じる
sock.close()
