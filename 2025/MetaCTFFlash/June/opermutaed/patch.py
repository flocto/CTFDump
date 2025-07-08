data = open('opermutated', 'rb').read()
patch = open('dump.bin', 'rb').read()

# print(hex(data.find(b'\x13\xd9\x90Z\x13\xd9')))

start = 0x86180
length = 0x105c

data = data[:start] + patch[:length] + data[start + length:]
with open('opermuted_patched', 'wb') as f:
    f.write(data)