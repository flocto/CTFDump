from PIL import Image

# img = Image.open('secret.png')
img = Image.open('DSCF3911.jpg')
# DSCF3911.jpg

width, height = img.size

lsb = []

for x in range(5):
    for y in range(height):
        pixel = list(img.getpixel((x, y)))
        for i in range(3):
            lsb.append(pixel[i] & 1)

b = bytearray()
for i in range(0, len(lsb), 8):
    b.append(int(''.join(map(str, lsb[i:i+8][::-1])), 2))

b = b.replace(b'\x00', b'')
print(b[:100])