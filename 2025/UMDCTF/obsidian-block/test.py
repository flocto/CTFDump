from Crypto.Util.number import bytes_to_long
import os

def rot(n, r):
    return (n >> r) | ((n << (256 - r) & (2**256 - 1)))

round_constants = [3, 141, 59, 26, 53, 58, 97, 93, 23, 84, 62, 64, 33, 83, 27, 9, 50, 28, 84, 197, 169, 39, 93, 75]

M = 2**256

def encrypt(key, block):
    for i in range(1):
        block = (block + key) % M
        block = rot(block, round_constants[i])
    return block

key = (1 << 253) | bytes_to_long(os.urandom(31))
print(bin(key)[2:].zfill(256))
block = (7 << 253) | bytes_to_long(os.urandom(31))
print(bin(block)[2:].zfill(256))

outside = (encrypt(key, 0) + encrypt(0, block)) % M
inside = encrypt(key, block)
print(bin(outside)[2:].zfill(256))
print(bin(inside)[2:].zfill(256))  
print(bin(outside ^ inside)[2:].zfill(256))
