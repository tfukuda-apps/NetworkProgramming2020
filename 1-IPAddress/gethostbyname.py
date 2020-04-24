# -*- coding: utf-8 -*-
"""
gethostbyname.pyプログラム
ホスト名をIPアドレスに変換するプログラム
使い方　>python gethostbyname.py
"""

# モジュールのインポート
import socket

# メイン実行部
# 繰り返し処理
while True:
    try:
        hostname = input("ホスト名を入力（qで終了）")
        if hostname == "q": # 終了
            break
        print(socket.gethostbyname(hostname))
    except:
        print("変換できませんでした")
# gethostbyname.pyの終わり
