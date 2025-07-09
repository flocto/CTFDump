import socket
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Util.number import long_to_bytes, bytes_to_long
import struct

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '34.30.123.169'
port = 6000

s.connect((host, port))

def send_message(opt, msg, known_length=None):
    # %c%06d
    if known_length:
        header = f'{opt}{known_length:06d}'.encode() + b'\x00'
    else:
        header = f'{opt}{len(msg):06d}'.encode() + b'\x00'
    assert len(header) == 8, "Header length must be 8 characters"
    s.send(header)
    if known_length:
        msg = msg.ljust(known_length, b'\x00')
    s.send(msg)

def receive_message(known_length=None):
    header = s.recv(8)
    # print(f'Received header: {header}')
    opt = chr(header[0])
    length = int(header[1:-1].strip())
    if known_length:
        msg = s.recv(known_length)
        while len(msg) < known_length:
            more = s.recv(known_length - len(msg))
            if not more:
                break
            msg += more
    else:
        msg = s.recv(length)
    return opt, msg

def list_messages():
    send_message('l', b'a')
    opt, num_notes = receive_message()
    assert opt == 'n', "Expected 'n' response for list messages"
    assert len(num_notes) == 8, "Expected 8 bytes for number of notes"
    num_notes = struct.unpack('<Q', num_notes)[0]
    print(f'Number of messages: {num_notes}')
    for i in range(min(10, num_notes)):
        opt, msg = receive_message(known_length=0x428)
        # print(opt, msg, len(msg))
        iv = msg[:16]
        key = msg[16:32]
        msg_len = struct.unpack('<I', msg[32:36])[0]
        # print(msg_len)
        encrypted_msg = msg[36:36 + msg_len]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_msg = cipher.decrypt(encrypted_msg)
        decrypted_msg = unpad(decrypted_msg, AES.block_size)
        print(i + 1, decrypted_msg)

def add_message(msg):
    iv  = b'supersecretiv123'
    key = b'supersecretkey23'
    msg_len = len(msg)

    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_msg = pad(msg, AES.block_size)
    encrypted_msg = cipher.encrypt(padded_msg)
    encrypted_msg = encrypted_msg
    
    prefix = iv + key + struct.pack('<I', msg_len)
    assert len(prefix) == 0x24
    full_msg = prefix + encrypted_msg
    full_msg = full_msg.ljust(0x428, b'\x00')
    send_message('a', full_msg, known_length=0x428)

for i in range(22):
    add_message(b'A')
list_messages()

s.close()