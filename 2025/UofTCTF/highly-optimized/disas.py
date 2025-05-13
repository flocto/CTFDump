import struct
data = open('highly-optimized', 'rb').read()
start = 0x3020
leng = 0x109
data = struct.unpack('<' + 'Q' * (leng), data[start:start + leng * 8])

disas = []
i = 0
pushes = []

while data[i] != 6:
    match data[i]:
        case 0:
            arg = data[i + 1]
            disas.append(f'push {arg}')
            pushes.append(arg)
            i += 2
        case 1:
            disas.append('dup')
            i += 1
        case 2:
            disas.append('sub')
            i += 1
        case 3:
            disas.append('less')
            i += 1
        case 4:
            disas.append(f'jnz -{data[i + 1]}')
            i += 2
        case 5:
            disas.append('out')
            i += 1
        case 6:
            disas.append('end')
            break

for i, instr in enumerate(disas):
    print(f'{i:02d}: {instr}')

f = ''
for i in range(0, len(pushes), 3):
    f += chr(pushes[i] % pushes[i + 1])

print(f)