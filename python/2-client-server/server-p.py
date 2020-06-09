import socket
import signal
import multiprocessing

# キーボードからの[ctrl]+[c]を非同期で受付
signal.signal(signal.SIGINT, signal.SIG_DFL)

'''
commun関数
  クライアントとの通信用関数
引数：
  sock_c  通信用のソケットオブジェクト
  addr    クライアントのアドレス情報
'''


def commun(sock_c, addr):
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


# 待受に使うIPアドレスとポート番号
MY_ADDRESS = ""
MY_PORT = 50000
# 受信用バッファサイズ
BUFSIZE = 256

if __name__ == "__main__":

    # ソケットを作成
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 自分の情報をソケットに登録
    sock.bind((MY_ADDRESS, MY_PORT))
    # ソケットを待ち受け状態にする
    sock.listen()

    while True:
        # 接続要求→受理
        sock_c, addr = sock.accept()
        # スレッドの作成と開始
        p = multiprocessing.Process(target=commun, args=(sock_c, addr))
        p.start()

    # 待ち受け用ソケットを閉じる
    sock.close()
