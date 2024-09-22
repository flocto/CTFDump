# print(hash(hash(id(object()))))

if eval(__import__('regex').fullmatch(r'[a-z]+\(((?R)|)\)', input('> '))[0]) == 0x1337133713371337:
    print(open('flag.txt', 'r').read())

