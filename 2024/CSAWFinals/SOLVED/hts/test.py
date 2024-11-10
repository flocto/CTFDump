header = open('header.txt', 'rb').read()
body = open('body.txt', 'rb').read()
chunks = [body[i:i+16] for i in range(0, len(body), 16)]

from collections import Counter

c = Counter(chunks)
# print(c.most_common(10))
for b, cnt in c.most_common(10):
    print(cnt, b)

white = [x[0] for x in c.most_common(3)]
grey = [x[0] for x in c.most_common()[3:6]]
dark_grey = [x[0] for x in c.most_common()[7:10]]

print(b''.join(white)[:16].hex())

out_chunks = []
for i, chunk in enumerate(chunks):
    if chunk in white:
        out_chunks.append(b'\xff' * 16)
    elif chunk in grey:
        # out_chunks.append(b'\x00' * 16)
        out_chunks.append((b'\x35\x35\x35' * 5) + b'\x35')
    elif chunk in dark_grey:
        # out_chunks.append(b'\x00' * 16)
        out_chunks.append((b'\x1a\x1a\x1a' * 5) + b'\x1a')
    else:
        out_chunks.append(chunk)

c = Counter(out_chunks)
# print(c.most_common(10))
for b, cnt in c.most_common(10):
    print(cnt, b)

open('dump/test.bmp', 'wb').write(header + b''.join(out_chunks))