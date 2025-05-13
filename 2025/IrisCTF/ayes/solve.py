from pwn import remote, process
from tqdm import trange
import aes
import os

def randblock():
    return os.urandom(16)

# nc ayes.chal.irisc.tf 10100
r = remote('ayes.chal.irisc.tf', 10100)
# r = process(['python3', 'chal.py'])

r.sendlineafter(b'> ', b'663') # sbox now has no 0

bits = list(bin(int.from_bytes(bytes(aes.s_box), "big"))[2:].rjust(256 * 8, '0'))
bits[663] = "1" if bits[663] == "0" else "0"
sbox = int(''.join(bits), 2).to_bytes(256, "big")

byts = set(range(256))
seen = [set() for _ in range(16)]

payloads = [randblock().hex().encode() for _ in range(4000)]
r.sendline(b"\n".join(payloads[:1000]))
r.recvline()
for _ in trange(1000):
    enc = bytes.fromhex(r.recvline().strip().decode()[2:])
    for i in range(16):
        seen[i].add(enc[i])
    if all(len(s) == 255 for s in seen):
        break 

r.sendline(b"\n".join(payloads[1000:2000]))
for _ in trange(1000):
    enc = bytes.fromhex(r.recvline().strip().decode()[2:])
    for i in range(16):
        seen[i].add(enc[i])
    if all(len(s) == 255 for s in seen):
        break 

r.sendline(b"\n".join(payloads[2000:3000]))
for _ in trange(1000):
    enc = bytes.fromhex(r.recvline().strip().decode()[2:])
    for i in range(16):
        seen[i].add(enc[i])
    if all(len(s) == 255 for s in seen):
        break 

r.sendline(b"\n".join(payloads[3000:]))
for _ in trange(1000):
    enc = bytes.fromhex(r.recvline().strip().decode()[2:])
    for i in range(16):
        seen[i].add(enc[i])
    if all(len(s) == 255 for s in seen):
        break 

round_key = b''.join([byts.difference(s).pop().to_bytes(1, 'big') for s in seen])
print(round_key)

rcon = [x.to_bytes(4, 'little') for x in [ 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36, ]]

def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

def sub_bytes(state):
    return bytes(sbox[b] for b in state)

def rot_word(word):
    return word[1:] + word[:1]

for i in range(10): # going backwards
    w = [round_key[0:4], round_key[4:8], round_key[8:12], round_key[12:16]]

    prev_w = [
        xor_bytes(w[3], w[2]),
        xor_bytes(w[2], w[1]),
        xor_bytes(w[1], w[0]),
    ]

    prev_w.append(
        xor_bytes(w[0], xor_bytes(sub_bytes(rot_word(prev_w[0])), rcon[9 - i]))
    )

    round_key = b''.join(prev_w[::-1])

print(round_key)
a = aes.AES(round_key)
key_dec = a.decrypt_block(round_key)
print(key_dec)

r.sendlineafter(b'> ', key_dec.hex())
r.interactive()