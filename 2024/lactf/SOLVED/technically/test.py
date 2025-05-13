data = open('technically_correct', 'rb').read()

target = b'\x31\xed'

donor = open('meow', 'rb').read()

s = 0
s = data.find(target, s)
s = data.find(target, s+1)
s = data.find(target, s+1)

carved = data[data.find(target, s + 1):data.find(target, s + 1) + 0x1000]

donor = donor[:0x1140] + carved + donor[0x1140 + len(carved):]
open('donor', 'wb').write(donor)
