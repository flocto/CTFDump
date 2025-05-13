data = open('Chal.exe', 'rb').read()

start = data.find(b'\x6f\x71\xb2\xcd\x71\xba')
size = 0xe00

dat = data[start:start+size]
dat = bytes([d ^ 0x39 for d in dat])
open('dump.bin', 'wb').write(dat)