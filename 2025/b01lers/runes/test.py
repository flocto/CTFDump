f = [
    18376,
    48276,
    23846,
    15298,
    23826,
    16283,
    68273,
    72376,
    37512,
    17332,
    17352,
    17392,
    62387,
    32739,
    58373,
    27372
]

x = f[0]
for i in range(1, len(f)):
    x *= f[i]
x += 9783

x_parts = []
while x:
    x_parts.append(x % 128)
    x //= 128
print(x_parts, len(x_parts))

h = 76313276953287674717995179101369411534359846914017972013351828426419897
enc = []
while h:
    enc.append(h % 128)
    h //= 128

print(enc, len(enc))

precomp = [None] * 127
for i in range(128):
    precomp[pow(3, i, 127)] = i

enc = [precomp[i] for i in enc]
print(enc, len(enc))

dec = [enc[i] ^ x_parts[i] for i in range(len(enc))]
print(bytes(dec))