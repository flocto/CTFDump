banned = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ`~=+[]{}|!@#$%&()>< "

def check(x):
    return all(i not in banned and ord(i) < 128 for i in x)

x = 'random string'

inp = '''banned'''

if not check(inp):
    print('you are not ready for it')

print(eval(inp[:1337]))


target = (1337, 420, 69, 2396745, 57005, 48879, 51966, 14600926, 1784768876, 3735928559, 322376503, 4886718345, 123456789, 13371337, 1099)
allowed = '\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f"\'*,-./:;?\\^_abcdefghijklmnopqrstuvwxyz\x7f'
 
# print(bytes.__dict__)