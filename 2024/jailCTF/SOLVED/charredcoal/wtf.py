msg = '“'

print(msg.encode(), ord(msg), ''.join(chr(i) for i in msg.encode()), ''.join(chr(i) for i in msg.encode()).encode())

inp = bytes.fromhex('515215').decode()
input=inp.encode()
print(input)