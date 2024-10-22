data = open('printf_patched', 'rb').read()

start = 0x2008
length = 0x168a2

rep = b"%1$'0.0E%1$+0.0E%1$-0.0E%1$ 0.0E%1$#0.0E\x00"
data = data[:start] + rep + data[start+len(rep):]

open('printf_patched2', 'wb').write(data)