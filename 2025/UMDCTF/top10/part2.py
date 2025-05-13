import struct
import ctypes
def bits_to_fp(x):
    return struct.unpack('<f', struct.pack('<I', x))[0]

def fp_to_bits(f):
    return struct.unpack('<I', struct.pack('<f', f))[0]

x = 0x34c25f30675f2f906e5f33776e5f2ffa
x = x.to_bytes(16, 'little')
floats = struct.unpack('<4f', x)
print(floats)
a, b, c = floats[:3]
a, b, c = [ctypes.c_float(f).value for f in floats[:3]]
f3 = floats[3] / 2

f1 = bits_to_fp(int.from_bytes(b'33d_', 'little'))

f0 = b - f1

# a = f2 - f1
# b = f1 + f0
# c = f0 - f2

# a + b + c = 2 * f0
# f0 = (a + b + c) / 2
# b = f1 + f0
# f1 = b - f0
# c = f0 - f2
f2 = f0 - c

prod = 0x54ad43a6
prod = bits_to_fp(prod)
print(prod)
# prod = f1 * f3
f3 = prod / f1


f0, f1, f2 = [ctypes.c_float(f).value for f in (f0, f1, f2)]
x0, x1, x2 = fp_to_bits(f0), fp_to_bits(f1), fp_to_bits(f2)
print(hex(x0), hex(x1), hex(x2))
print(x0.to_bytes(4, 'little'))
print(x1.to_bytes(4, 'little'))
print(x2.to_bytes(4, 'little'))

x3 = fp_to_bits(f3)
print(x3.to_bytes(4, 'little')) 
