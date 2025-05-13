from tea import TEA
import struct
import subprocess
import time

key_parts = [0xa341316c, 0xc8013ea4, 0x3c6ef372, 0x14292967]
key = struct.pack("<4L", *key_parts)

data = open('real_flag_enc', 'rb').read()    
data = bytearray(data) * 10
n = len(data)

for i in range(n):
    data[i] ^= i & 0xff

print('starting tea')
open('flag_enc_cpp2', 'wb').write(data)
start = time.time()
subprocess.check_output(['./teabrute'])
data = open('flag_dec_cpp2', 'rb').read()
data = bytearray(data)

print('tea done', time.time() - start)

# undo part4
BLOCK_SIZE = 256
for B in range(0, n, BLOCK_SIZE):
    for i in range(0, BLOCK_SIZE, 2):
        j = (i - 1) % BLOCK_SIZE    
        data[B + j], data[B + i] = data[B + i], data[B + j]

# print(data.hex())

# undo part3
for B in range(0, n, BLOCK_SIZE):
    for i in range(0, BLOCK_SIZE, 2):
        j = (i + 1) % BLOCK_SIZE
        data[B + j], data[B + i] = data[B + i], data[B + j]

# print(data.hex())

# undo part2
for B in range(0, n, BLOCK_SIZE):
    # for i in range(BLOCK_SIZE):
    #     data[B + i] = data[B + i] ^ data[B + (i + 1) % BLOCK_SIZE] ^ 172
    for i in range(BLOCK_SIZE - 1, -1, -1):
        data[B + i] = data[B + i] ^ data[B + (i + 1) % BLOCK_SIZE] ^ 172

# print(data.hex())

# undo part1
step1_sbox = list(bytes.fromhex('e24a652b5ca8906a6063f5e1989775300f57b338eb463629fbc4db2674fc1270399e227205a1156ef78f93d69b7e3443b9f2d4d2d195c2f8cc4e3e07aeba006b21a01a5d19e6e73755eab141ef5f246d42f435bc7a847fc9141087ec9cf9e361becda4de7b77038ae9d98d966cfe1f4cdd6208a578b5e453af3bd7281e4bd55076548c11e0cedf859259fdbfa6c0684d8b203dad94f131a24751c3bb86230c2558b45e172d69ff8e01c1aa67fa2f32e5c5cab22e8818c7890244490d9f71a3a980f0b09d73f681cb2799d0e804dcbd454f641c0b7db8a7f316569ad33c5b06096fb7cf1dee3a135a91ab0e7983da82332c0ab62a66c81bac48edd87c403f52c6'))
step1_isbox = [step1_sbox.index(i) for i in range(256)]
def step1_shuffle(v, i):
    b = (v ^ (i * 73 + 172)) & 0xffff
    c = ((b & 240) >> 4) & 0xffff
    d = (b << 4) & 0xffff
    return (c | d) & 0xff

def step1_find_val(goal, idx):
    for i in range(256):
        a = step1_shuffle(i, idx)
        if a == goal:
            return i
    assert False

def step1_enc(data):
    return bytes([step1_sbox[step1_shuffle(a,i)] for i,a in enumerate(data)])

def step1_denc(data):
    return bytes([step1_find_val(step1_isbox[a], i) for i,a in enumerate(data)])

data = step1_denc(data)
open('real_flag.png', 'wb').write(data)