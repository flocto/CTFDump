import socket
import random

from ecutils.core import EllipticCurve, Point
from Crypto.Cipher import ChaCha20
from hashlib import sha512

q = 0xc90102faa48f18b5eac1f76bb40a1b9fb0d841712bbe3e5576a7a56976c2baeca47809765283aa078583e1e65172a3fd
a = 0xa079db08ea2470350c182487b50f7707dd46a58a1d160ff79297dcc9bfad6cfc96a81c4a97564118a40331fe0fc1327f
b = 0x9f939c02a7bd7fc263a4cce416f4c575f28d0c1315c4f0c282fca6709a5f9f7f9c251c9eede9eb1baa31602167fa5380
gx = 0x087b5fe3ae6dcfb0e074b40f6208c8f6de4f4f0679d6933796d3b9bd659704fb85452f041fff14cf0e9aa7e45544f9d8
gy = 0x127425c1d330ed537663e87459eaa1b1b53edfe305f6a79b184b3180033aab190eb9aa003e02e9dbf6d593c5e3b08182
n = 30937339651019945892244794266256713890440922455872051984762505561763526780311616863989511376879697740787911484829297

G = Point(gx, gy)
cv = EllipticCurve(q, a, b, G, n, 1)
k = random.randint(1, n-1)
P = cv.multiply_point(k, G)

xorkey = 0x133713371337133713371337133713371337133713371337133713371337133713371337133713371337133713371337

def encrypt_thing(dat):
    return dat ^ xorkey

def parse_bytearray(dat):
    return int.from_bytes(dat, 'big')

def pack_bytearray(n):
    return n.to_bytes((n.bit_length() + 7) // 8, 'big')

def send_enc_string(skt: socket.socket, cipher, dat):
    skt.send(cipher.encrypt(dat + b'\x00'))

def recv_enc_string(skt: socket.socket, cipher):
    return cipher.encrypt(skt.recv(1024))

def server_program():
    host = '192.168.56.103'
    port = 31337  

    server_socket = socket.socket() 
    server_socket.bind((host, port))  

    server_socket.listen(2)
    conn, address = server_socket.accept()  
    print("Connection from: " + str(address))

    x = conn.recv(1024)
    x = encrypt_thing(parse_bytearray(x))
    y = conn.recv(1024)
    y = encrypt_thing(parse_bytearray(y))
    other = Point(x, y)

    conn.send(pack_bytearray(encrypt_thing(P.x)))
    conn.send(pack_bytearray(encrypt_thing(P.y)))

    shared = cv.multiply_point(k, other)
    print(shared)

    hsh = sha512(pack_bytearray(shared.x)).digest()
    key = hsh[:32]
    nonce = hsh[32:40]
    print(key, nonce)

    cipher = ChaCha20.new(key=key, nonce=nonce)
    send_enc_string(conn, cipher, b'verify')

    verify = recv_enc_string(conn, cipher)
    print(verify)

    while True:
        data = input(' -> ').encode()
        send_enc_string(conn, cipher, data)

        data = recv_enc_string(conn, cipher)
        if not data:
            break

        print('Received:', data)

    conn.close()  


if __name__ == '__main__':
    server_program()