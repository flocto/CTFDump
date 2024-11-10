from PIL import Image
from collections import Counter
import random

img = Image.open('dump.bmp')

header = open('header.txt', 'rb').read()
body = open('body.txt', 'rb').read()

w, h = img.size

print(w, h)

blocks = Counter()

line_size = w*3+1
special = b''
for i in range(h):
    line = body[i*line_size:i*line_size+line_size]
    special = line[-16:]
    assert len(line) % 16 == 0
    for j in range(0, len(line), 16):
        blocks[line[j:j+16]] += 1

print(len(blocks)) 

rand_map = {}
for c in blocks:
    rand_map[c] = bytes([random.randint(0, 255), random.randint(0, 255)]) * 8

out = []
for i in range(0, len(body), 16):
    block = body[i:i+16]
    if block == special:
        out.append(b'\xf3\xfe\xff' * 5 + b'\xf3')
    else:
        out.append(rand_map[block])

open('dump/dump2.bmp', 'wb').write(header + b''.join(out))