data = open('flag.bmp', 'rb').read()

data = data[0x164:]

head, data = data[:0x20], data[0x20:]

head = [h & 1 for h in head]
head = int(''.join(map(str, head)), 2)
length = int.from_bytes(head.to_bytes(4, 'little'), 'big')

bits = []
for d in data[:length * 8]:
    bits.append(d & 1)

dat = [
    int(''.join(map(str, bits[i:i+8])), 2)
    for i in range(0, len(bits), 8)
]

open('flag.bin', 'wb').write(bytes(dat))