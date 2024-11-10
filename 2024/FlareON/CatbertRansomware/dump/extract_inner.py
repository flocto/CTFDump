data = open('DilbootApp.efi', 'rb').read()

start = 0x5ce0
size = 51261

inner = data[start:start+size]
open('your_mind.jpg.c4tb', 'wb').write(inner)