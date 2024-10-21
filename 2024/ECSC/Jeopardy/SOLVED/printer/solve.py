from pwn import process, remote
import base64
import os
import qrcode
import struct
from PIL import Image

data = 'WA33INAR7JDKUPNJ'
qr = qrcode.make(data, box_size=2)
#resize to 100x100
qr = qr.resize((100, 100))
qr.save('qr.png')


# data = (b'S\x0bA\x00A\x00\x00\x00' + 
#         b'S\x0dA\x00C\x00\x00\x00')
        # b'S\x001\x00Z\x00\x00\x00'+
        # b'S\x0d\x1e\x00Z\x00\x00\x00')
        # b'S\x1e\x1e\x002\x00\x00\x00'+
        # b'S\x1e<\x002\x00\x00\x00S\x1e<\x00Z\x00\x00\x00S\x02<\x00Y\x00\x00\x00S\x1e<\x002\x00\x00\x00S\x1e-\x00\x1e\x00\x00\x00S\x1e\x1e\x002\x00\x00\x00S\x1e\x1e\x00Z\x00\x00\x00S\x02(\x00Z\x00\x00\x00S\x02(\x00Y\x00\x00\x00S\x1b(\x00K\x00\x00\x00S\x1b2\x00K\x00\x00\x00S\x1b2\x00Z\x00\x00\x00') 

# data = b'K\'

# open('data.t', 'wb').write(base64.b64encode(data))

img = Image.open('qr.png')

white = b'\x00'
black = b'\x0b'

pixs = img.load()
commands = []
color = 1
for row in range(14, 86):
#     print(''.join(['#' if pixs[col, row] == 0 else ' ' for col in range(14, 86)]))
    col = 14
    while col < 86:
        if pixs[col, row] == 0:
            count = 0
            while col < 86 and pixs[col, row] == 0:
                count += 1
                col += 1
            commands.append((black, row, col))
            # color = not color
        else:
            count = 0
            while col < 86 and pixs[col, row] == 255:
                count += 1
                col += 1
            commands.append((white, row, col))
            # color = not color
    commands.append((white, row+1, col))
    commands.append((white, row+1, 14))
    # break   

print(commands)

data = b'S\x00\x0d\x00\x0d\x00\x00\x00'
for command in commands:
    data += b'S' + command[0] + struct.pack('<H', command[2]) + struct.pack('<H', command[1]) + b'\x00\x00'

open('test.t', 'wb').write(data)

data = base64.b64encode(data)
# print(data, len(data))
# nc printer.challs.jeopardy.ecsc2024.it 47020
p = remote('printer.challs.jeopardy.ecsc2024.it', 47020)

# p = process(['server.py'], level='error', cwd=os.path.join(os.path.dirname(__file__), 'src'))
p.sendline(data)
print(p.recvall())