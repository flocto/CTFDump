dat = open('extracted/example.ql', 'rb').read().split(b'\n')

for line in dat:
    parts = line.split(b' ')
    print(parts)