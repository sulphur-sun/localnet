import socket
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hostname = socket.gethostname()
HOST = socket.gethostbyname(hostname)
print("name, host: ", hostname, HOST)

try:
    PORT = int(sys.argv[1])
except Exception as ex:
    PORT = 8080


def main():
    s.bind((HOST, PORT))
    s.listen(10)
    print('server listening on port {}...'.format(PORT))

    conn, _ = s.accept()
    while True:
        cmd = input('> ').rstrip()
        conn.send(bytes(cmd, encoding="utf-8", errors="ignore"))

        if cmd == 'exit':
            s.close()
            sys.exit(0)

        elif cmd == 'ls' or cmd == 'cd':
            data = recv_data(conn)
            print(str(data, encoding="utf-8", errors="ignore"))

        elif cmd[:7] == "getfile": 
            f = open(cmd[8:], "w")
            data = recv_data(conn).decode("utf-8")
            f.write(data)
            f.close()
        else:
            continue

def recv_data(conn):
    datalen = int.from_bytes(conn.recv(4), "big")
    data = conn.recv(datalen)
    return data


if __name__ == '__main__':
    main()
