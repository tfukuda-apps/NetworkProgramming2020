import datetime

# 受信用バッファサイズ
BUFSIZE = 1024
# クライアントからの応答を待つ時間
WAIT_TIME = 1

def recv_crlf(sock_c):
    # 1文字ずつ受信する
    BUFSIZE_CRLF = 1

    req = ""
    # CRLFが見つかるor通信終了まで受信を続ける
    while req.find("\r\n") < 0:
        data = sock_c.recv(BUFSIZE_CRLF)
        if not data:  # 受信失敗（通信終了）
            break
        req += data.decode("UTF-8")
    
    return req

def get_request(sock_c):
    # クライアントからの応答なしに備えて時間制限を設ける
    sock_c.settimeout(WAIT_TIME)

    # 戻り値（Request-Line, Header, Message Body）
    req_l = req_h = req_m = None

    try:
        # Request Lineの取得
        req = recv_crlf(sock_c)
        # CRLFが何文字目にあるのかを確認
        i_CRLF = req.find("\r\n")
        if i_CRLF < 0:
            # 受信失敗（CRLFが見つからない）
            print("No Request Line")
            return (None, None, None)
        # 受信成功　→　request lineの抜き取り
        req_l = req[:i_CRLF]

        # Request Hedaerの取得
        req_h = {}
        key_value = recv_crlf(sock_c)
        while key_value != "\r\n":
            k, v = key_value.split(": ")
            req_h[k] = v[:-2]
            key_value = recv_crlf(sock_c)

        # Message Bodyの取得
        if "Content-Length" in req_h:
            req_m = sock_c.recv(BUFSIZE).decode("UTF-8")
            while len(req_m) < int(req_h["Content-Length"]):
                data = sock_c.recv(BUFSIZE)
                if not data:
                    break
                req_m += data.decode("UTF-8")
    except:
        pass

    return (req_l, req_h, req_m)

def send_response(sock_c, code, phrase, f):
    statusline = "{} {} {}".format("HTTP/1.1", code, phrase)

    dt_now = datetime.datetime.now()
    header = dt_now.strftime("Date: %a, %d %m %Y %H:%M:%S JST\r\n")

    if f != None:
        body = f.read()
        header += "Content-Length: {}\r\n".format(len(body))

        extention_index = f.name.rindex(".")
        extension = f.name[-extention_index + 1:].lower()

        if extension == "html" or extension == "htm":
            header += "Content-Type: {}\r\n".format("text/html")
        elif extension == "txt":
            header += "Content-Type: {}\r\n".format("text/plain")
        elif extension == "gif":
            header += "Content-Type: {}\r\n".format("image/gif")
        elif extension == "png":
            header += "Content-Type: {}\r\n".format("image/png")

    sock_c.sendall(statusline.encode("UTF-8"))
    sock_c.sendall(header.encode("UTF-8"))
    sock_c.sendall("\r\n".encode("UTF-8"))
    if body != None:
        sock_c.sendall(body)

