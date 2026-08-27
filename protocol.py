from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Hash import HMAC, SHA256

def generate_key(socket):
    aes_key = get_random_bytes(16)
    send_data(aes_key, socket)
    return aes_key

def send_data(data, socket):
    if not isinstance(data, bytes):
        data = data.encode("utf-8")
    length = len(data)
    try:
        socket.sendall(length.to_bytes(4, 'big'))
        socket.sendall(data)
    except Exception as e:
        raise

def recv_data(conn):
    datalen = int.from_bytes(conn.recv(4), "big")
    data = b''
    while len(data) < datalen:
        chunk = conn.recv(min(4096, datalen - len(data)))
        if not chunk:
            break
        data += chunk
    return data

def encrypt_file(key, file):
    cipher = AES.new(key, AES.MODE_GCM)
    with open(file, 'rb') as file:
        plaintext = file.read()
        file.close()
    text, tag = cipher.encrypt_and_digest(plaintext)
    return cipher.nonce, tag, text
    
def decrypt_file(key, nonce, tag, text):
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    data = cipher.decrypt_and_verify(text, tag)
    return data