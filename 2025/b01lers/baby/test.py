def l2b(x):
    return x.to_bytes(8, 'little')


# print(l2b(2410660987913006915))
# print(l2b(2851477885252183))

# print(l2b(7526676552943431237))
# print(l2b(2322282225991032933))

enc = b''
# print(l2b(4228116579593854571))
# print(l2b(16903143109589003699))
enc += l2b(4228116579593854571)
enc += l2b(16903143109589003699)
# print(l2b(13507378150930045739))
# print(l2b(8173535459512591702))
enc += l2b(13507378150930045739)
enc += l2b(8173535459512591702)

# print(l2b(72057594037927940))

# print(list(enc))

enc = list(enc)

enc = [(x * pow(173, -1, 256)) % 256 for x in enc]
print(enc)

for i in range(31, 0, -1):
    enc[i] = (enc[i] - enc[i - 1]) % 256
print(enc)

swaps = []
for i in range(32):
    swaps.append((i, (i * i + 7) % 32))

for swap in swaps[::-1]:
    enc[swap[0]], enc[swap[1]] = enc[swap[1]], enc[swap[0]]
print(enc)

print(bytes(enc))