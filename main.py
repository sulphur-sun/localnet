import socket
import sys
from protocol import send_data, recv_data, generate_key, encrypt_file, decrypt_file

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
    key = generate_key(conn)

    while True:
        cmd = input('> ').rstrip()
        conn.send(bytes(cmd, encoding="utf-8", errors="ignore"))

        if cmd == 'exit':
            s.close()
            sys.exit(0)

        elif cmd == 'ls' or cmd.startswith('cd '):
            data = recv_data(conn)
            print(str(data, encoding="utf-8", errors="ignore"))

        elif cmd[:7] == "getfile": 
            nonce = recv_data(conn)
            tag = recv_data(conn)
            text = recv_data(conn)
            try:
                file = decrypt_file(key, nonce, tag, text)
                with open(cmd[8:], "wb") as f:
                    f.write(file)
            except Exception as e:
                raise

        elif cmd[:8] == 'sendfile':
            nonce, tag, text = encrypt_file(key, cmd[9:])
            send_data(nonce, conn)
            send_data(tag, conn)
            send_data(text, conn)

        else:
            continue

if __name__ == '__main__':
    main()
