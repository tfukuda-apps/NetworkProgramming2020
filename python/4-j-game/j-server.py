# exe化は
# pyinstaller j-server.py --onefile
# で行っている
import socket
import signal
import threading
import random

# キーボードからの[ctrl]+[c]を非同期で受付
signal.signal(signal.SIGINT, signal.SIG_DFL)

'''
commun関数
  クライアントとの通信用関数
引数：
  sock_c  通信用のソケットオブジェクト
  addr    クライアントのアドレス情報
'''

CHARSET = "UTF-8"
BUFSIZE = 1024

card = {0: "やせ我慢", 1: "愛情", 2: "小切手"}

msg_error = "ルール通りに0～3を送ってくれなきゃ怒っちゃうぞっ！もういっかい入力してね！"
msg_ready = "---\n【{}回戦】　どの手にする？"
msg_client_lose = "あなた：{}<--->わたし：{}\nやった～わたしの勝ち！\n" + msg_ready
msg_client_win = "あなた：{}<--->わたし：{}\nあなたの勝ちかぁ！強いね！\n" + msg_ready
msg_client_even = "あなた：{}<--->わたし：{}\n引き分け！相性抜群かもね！\n" + msg_ready
msg_fin = "あら？終わるのね。あなたの戦績は{}勝{}敗{}分だったよ！じゃ～ね～！"

msg_opening = "今からJゲームを始めるよ！\n\n"
msg_opening += "------------------------------------------\n"
msg_opening += "【ルール説明】\n0～3の数字を送ってね。\n0->やせ我慢\n1->愛情\n2->小切手\n3->ゲーム終了\n"
msg_opening += "「やせ我慢」をしているヤンキーも「愛情」を見せられると弱さを見せちゃうよ。\nでも「愛情」も「小切手」を見せられると揺らいでしまうよ。\nただし、「小切手」を見せられたとしても「やせ我慢」でどうにかなるんだ。\nだから勝ち負けは下のような感じ。\n"
msg_opening += "「愛情」win-lose「やせ我慢」\n「小切手」 win-lose 「愛情」\n「やせ我慢」 win-lose 「小切手」\n\nじゃあはじめるよ～\n"
msg_opening += msg_ready.format(1)


def game(sock, addr):
    numWinClient = 0
    numLoseClient = 0
    numEvenClient = 0
    numBattle = 0

    print("{}から接続がありましたので、ゲームを開始します".format(addr))

    # 挨拶＆ルール送信
    try:
        sock.sendall(msg_opening.encode(CHARSET))
    except:
        print("sendall function failed(1).")
        sock.close()
        return

    # ゲーム開始
    while True:
        try:
            numBattle += 1

            # クライアントの「手」を受信
            data = sock.recv(BUFSIZE)

            # 文字列→数値に変換
            try:
                client = int(data.decode(CHARSET))
            except:
                # クライアントが数値以外を送信してきたため、再入力を促す
                sock.sendall(msg_error.encode(CHARSET))
                continue

            # クライアントが0～3以外の入力であれば再入力を促す
            if client < 0 or 3 < client:
                sock.sendall(msg_error.encode(CHARSET))
                continue

            # 3を受信で正常終了（ループを抜けて最終結果を送信）
            if client == 3:
                break

            # 自分の「手」をランダムに0-2の整数で決める
            server = random.randint(0, 2)

            #
            # じゃんけんの勝敗決定アルゴリズム：
            # （自分-相手+3）を3で割った余り（剰余）が
            # 0　→　引き分け
            # 1　→　自分の勝ち
            # 2　→　相手の勝ち
            # となる
            #
            battle = (server - client + 3) % 3

            if battle == 0:
                # 引き分け
                numEvenClient += 1
                sock.sendall(msg_client_even.format(
                    card[client], card[server], numBattle+1).encode(CHARSET))
            elif battle == 1:
                # サーバの勝ち
                numLoseClient += 1
                sock.sendall(msg_client_lose.format(
                    card[client], card[server], numBattle+1).encode(CHARSET))
            elif battle == 2:
                # クライアントの勝ち
                numWinClient += 1
                sock.sendall(msg_client_win.format(
                    card[client], card[server], numBattle+1).encode(CHARSET))

        except:
            # 通信エラー（送信/受信）
            print("送受信エラーが発生したので{}との通信を終了します".format(addr))
            sock.close()
            return

    # 最終結果の通知
    try:
        sock.sendall(msg_fin.format(
            numWinClient, numLoseClient, numEvenClient).encode(CHARSET))
        sock.close()
    except:
        print("送受信エラーが発生したので{}との通信を終了します".format(addr))
        sock.close()
        return

    # 通信用ソケットを閉じる
    sock_c.close()


# 待受に使うIPアドレスとポート番号
MY_ADDRESS = ""
MY_PORT = 50000
# 受信用バッファサイズ
BUFSIZE = 256
VER = "2020-1"
msg_opening = "------------------------------------------\n"
msg_opening += "■■■■■■■■■■\n北九州工業高等専門学校　生産デザイン工学科　情報システムコース\n4年通年科目「ネットワークプログラミング」課題用プログラム　ver.{}。\n■■■■■■■■■■\n\n".format(
    VER)
msg_opening += "■　ゲームの概要\n　このゲームは0～2のうち一つの数字を互いに出して勝敗を決めるゲームだよ。\n"
msg_opening += "■　数字の対応\n　0->やせ我慢　　1->愛情　　2->小切手　　3->ゲーム終了\n"
msg_opening += "■　強い/弱いの規則\n"
msg_opening += "「やせ我慢」をしているヤンキーも「愛情」を見せられると弱さを見せちゃうんだ。\n→「やせ我慢」より「愛情」が強い\n"
msg_opening += "でも「愛情」も「小切手」を見せられると心が揺らいじゃうよ。\n→「愛情」より「小切手」が強い\n"
msg_opening += "ただ、「小切手」を見せられたとしても「やせ我慢」で耐えられるんだ。\n→「小切手」より「やせ我慢」が強い\n\n"
msg_opening += "■　クライアント作成のポイント\n1. サーバに接続\n2. ルールを受信して表示\n3.キーボードから入力した0～2の数字のどれかを送る\n4.サーバ側で計算された勝負結果が送られてくる\n（以後、勝負の繰り返し）\n※「3」を送るとゲーム終了となり、最終成績が送られてくる\n\nちなみに「3」を送るまではずっとゲームが続く神仕様だよ！\n"

print(msg_opening)
# ソケットを作成
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 自分の情報をソケットに登録
sock.bind((MY_ADDRESS, MY_PORT))
# ソケットを待ち受け状態にする
sock.listen()

print("さあポート{}で待ち受けてるよ！早く接続しにきてよ！".format(MY_PORT))
while True:
    # 接続要求→受理
    sock_c, addr = sock.accept()
    # スレッドの作成と開始
    p = threading.Thread(target=game, args=(sock_c, addr))
    p.start()

# 待ち受け用ソケットを閉じる
sock.close()
