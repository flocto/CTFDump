data = open('2024SCTF.wld', 'rb')

data.seek(0x94A830)

open('dump.bin', 'wb').write(data.read())