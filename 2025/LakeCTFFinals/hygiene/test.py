from pwn import *
from Crypto.Cipher import ChaCha20

key = open('keyfile', 'rb').read()
iv = b'\x00' * 0x8
cipher = ChaCha20.new(key=key, nonce=iv)
BLOCK_SIZE = 0x40
# r = process(['./chal', 'keyfile'])
# nc chall.polygl0ts.ch 9034
r = remote('chall.polygl0ts.ch', 9034)

def enc(block, pt, len):
    r.sendlineafter(b'to do?\n', b'1')
    r.sendlineafter(b'to encrypt?\n', str(len).encode())
    r.sendlineafter(b'to encrypt?\n', str(block).encode())
    r.sendlineafter(b'to encrypt:\n', pt)
    # r.sendlineafter(b'to encrypt:\n', b'B' * 380)
    r.recvuntil(b' text:\n')
    return r.recvline().strip()

enc(3, b'', 150)
dec = enc(3, b'', 150)
dec = bytes.fromhex(dec.decode())
key = dec[112:144]
print(f'key: {key.hex()}')

# r.interactive()
r.sendlineafter(b'to do?\n', b'2')
ct = bytes.fromhex(r.recvline().strip().decode())

cipher = ChaCha20.new(key=key, nonce=iv)
pt = cipher.decrypt(ct)

print(pt)