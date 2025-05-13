from pwn import remote, process
# nc chall.polygl0ts.ch 9099
r = remote("chall.polygl0ts.ch", 9099)
# r = process(['./chal.py'])
r.recvline()
pow = r.recvline().decode().strip()
pow = process(['bash', '-c', pow]).recvline().decode().strip()
r.sendline(pow)

src = open('main.c').read()
for line in src.split('\n'):
    r.sendline(line)
r.sendline('EOF')

r.interactive()