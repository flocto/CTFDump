vars = 0x0000001b,0x00000026,0x00000057,0x0000005f,0x00000076,0x00000009

out = [0] * 6
for i in range(1, 256):
    c = 0
    t = i
    while i != 1:
        if i % 2 == 0:
            i = i // 2
        else:
            i = 3 * i + 1
        c += 1
    
    for j in range(6):
        if c == vars[j]:
            out[j] = t

print(bytes(out))