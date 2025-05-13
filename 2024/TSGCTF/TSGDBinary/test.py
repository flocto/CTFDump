import struct
import ctypes

enc = bytes.fromhex('42d31f3164feaea202ad05481cac96d5e6624b23b5d0f7a7ca56195908603aac757dc4050a8eb8074f793defad737938')

nums = struct.unpack('<' + 'Q' * (len(enc) // 8), enc)

nums = [
    ctypes.c_uint64(num - 0x89fc76aef8d6a8c3).value for num in nums
]

print([hex(n) for n in nums])