from pwn import remote

r = remote('o-wronly-51fec5df59ecb4f7.i.chal.irisc.tf', 1337, ssl=True)

r.interactive()