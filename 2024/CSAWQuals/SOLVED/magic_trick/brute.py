from pwn import process
from tqdm import tqdm

alpha = '_}abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
known = b'csawctf{'
enc = open('real_output.txt', 'rb').read()

while known[-1] != '}':
    for c in tqdm(alpha):
        p = process(['./chall_patched'], level='error')
        p.sendlineafter(b'Enter data: ', known + c.encode())
        p.recvline_contains(b'wait...')
        # wait for EOF
        p.recvall()
        p.close()

        out = open('output.txt', 'rb').read()
        # print(enc, out)
        if enc.startswith(out):
            known += c.encode()
            print(known.decode())
            break