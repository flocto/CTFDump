from pwn import remote
import string
# nc challenge.utctf.live 7150
r = remote('challenge.utctf.live', 7150)

def chksum(data):
    return sum(ord(c) for c in data) % (len(data)+1)

alphabet = "}_" + string.digits + string.ascii_letters + string.punctuation

def generate_chksumed(data, t = None):
    if t is None:
        t = len(data)
    c = sum(ord(c) for c in data)
    # (c + x) % (t + 2) = t
    # x = t - c
    x = (t - c) % (t + 2)
    # no newline or return
    while x < 32:
        x += (t + 2)
    return data + chr(x)

def encrypt(data):
    padded_data = generate_chksumed(data, len(data))
    chunked = padded_data[:chksum(padded_data)]
    assert chunked == data
    padded_data = padded_data.encode()
    # print(padded_data)
    r.recvuntil(b'Enter text to be encrypted: ')
    r.sendline(padded_data)
    x = int(r.recvline().strip(), 16)
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')

def print_blk(hex_blks, sz):
   for i in range(0, len(hex_blks), sz):
       print(hex_blks[i:i+sz], ' ', end='')
   print()


enc_len = 38

# BLOCK 1
# known = "utflag{st0p_r0ll"
# while len(known) < 16:
#     for c in alphabet:
#         test = known + c
#         padding = 'A' * (16 - len(test))
#         data = padding + test + padding
#         enc = encrypt(data)
#         blocks = [enc[i:i+16] for i in range(0, len(enc), 16)]
#         if blocks[0] == blocks[1]:
#             print(test, blocks[0].hex(), blocks[1].hex())
#             known += c
#             break

# BLOCK 2
# block1 = "utflag{st0p_r0ll"
# known = "1ng_y0ur_0wn_cry"
# while len(known) < 16:
#     for c in alphabet:
#         test = known + c
#         first_block = (block1 + test)[-16:]
#         padding = 'A' * (16 - len(test))
#         data = first_block + padding
#         enc = encrypt(data)
#         blocks = [enc[i:i+16] for i in range(0, len(enc), 16)]
#         if blocks[0] == blocks[2]:
#             print(first_block, blocks[0].hex(), blocks[2].hex())
#             known += c
#             break

# BLOCK 3
# block1 = "utflag{st0p_r0ll"
block2 = "1ng_y0ur_0wn_cry"
known = "pt0!!}"
while len(known) < 16:
    for c in alphabet:
        test = known + c
        second_block = (block2 + test)[-16:]
        padding = 'A' * (16 - len(test))
        data = second_block + padding
        enc = encrypt(data)
        blocks = [enc[i:i+16] for i in range(0, len(enc), 16)]
        if blocks[0] == blocks[3]:
            print(second_block, blocks[0].hex(), blocks[3].hex())
            known += c
            break

# utflag{st0p_r0ll1ng_y0ur_0wn_crypt0!!}